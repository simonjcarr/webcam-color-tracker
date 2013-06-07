from pyfirmata import ArduinoMega, util
from pyfirmata import SERVO
import time


board = ArduinoMega('com3')
board.digital[7].mode = SERVO

window_width = 600
window_height = 400

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def getValues():
    try:
        f = open('values.txt','r')
        values = f.read().split(':')
        f.close
        return values
    except:
        pass




lastValue = 1
camx = 50
servox = 90
while 1:
    lastValue = servox
    try:
        #print "I am here"
        
        camx, camy = getValues()
        camx = int(float(camx))
        camy = int(float(camy))
        
    except:
        pass
    #print "camx: ", camx, "servox:", servox
    if camx == -2:
        continue
    if camx == -1:
        servox = 90
    
    
    
    #If the object has moved of the screen come back to the middle
    if servox < 2 or servox > 179:
        servox = 90
    
    #distance from center
    if camx < (window_width / 2):
        distance = (window_width / 2) - camx
    else:
        distance = camx - (window_width / 2)
    
    
    speed = str(translate(distance,10,311,.05,.01))
    print "Speed = " + speed, "distance = ", str(distance)
    
    
    if distance > 50:
        if camx > window_width / 2:
            for i in range(servox,servox - 1,-1):
                servox -= 1
                board.digital[7].write(i)
                time.sleep(float(speed))
        if camx < window_width / 2:
            for i in range(servox,servox + 1,1):
                servox += 1
                board.digital[7].write(i)
                time.sleep(float(speed))
            

    





        
        
        
        


