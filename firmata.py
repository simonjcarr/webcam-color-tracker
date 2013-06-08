from pyfirmata import ArduinoMega, util
from pyfirmata import SERVO
import time


board = ArduinoMega('com3')
board.digital[7].mode = SERVO
board.digital[6].mode = SERVO
window_width = 650
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
servoy = 90
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
        servoy = 90
    
    
    
    #If the object has moved of the screen come back to the middle
    if servox < 2 or servox > 179 or servoy < 2 or servoy > 179:
        servox = 90
        servoy = 90
    
    #xdistance from centre
    if camx < (window_width / 2):
        xdistance = (window_width / 2) - camx
    else:
        xdistance = camx - (window_width / 2)
    
    #ydistance from centre
    if camy < (window_height / 2):
        ydistance = (window_height / 2) - camy
    else:
        ydistance = camy - (window_height / 2)
        
    xspeed = str(translate(xdistance,10,(window_width / 2),.05,.01))
    yspeed = str(translate(ydistance,10,(window_height / 2),.05,.01))
    #print "xSpeed = " + xspeed, "xdistance = ", str(xdistance)
    #print "ySpeed = " + yspeed, "ydistance = ", str(ydistance)
    
    if xdistance > 60:
        if camx > window_width / 2:
            for i in range(servox,servox - 1,-1):
                servox -= 1
                board.digital[7].write(i)
                time.sleep(float(xspeed))
        if camx < window_width / 2:
            for i in range(servox,servox + 1,1):
                servox += 1
                board.digital[7].write(i)
                time.sleep(float(xspeed))
    
    if ydistance > 60:
        if camy < window_height / 2:
            for i in range(servoy,servoy - 1,-1):
                servoy -= 1
                board.digital[6].write(i)
                time.sleep(float(xspeed))
        if camy > window_height / 2:
            for i in range(servoy,servoy + 1,1):
                servoy += 1
                board.digital[6].write(i)
                time.sleep(float(xspeed))
            

    





        
        
        
        


