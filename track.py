#! /usr/bin/env python 
 
import cv 
import time

color_tracker_window = "Preston HackSpace 2013 BarCamp Project" 
 
class ColorTracker: 
    x = 0
    y = 0
    
    def __init__(self): 
        cv.NamedWindow( color_tracker_window, 1 ) 
        self.capture = cv.CaptureFromCAM(0) 
        self.tracking = False
        self.lasttrack = None
        self.hang_around_seconds = 5
        
    def run(self): 
        count = 0
        while True: 
            
            img = cv.QueryFrame( self.capture ) 
            img2 = cv.QueryFrame(self.capture)           
            #blur the source image to reduce color noise 
            cv.Smooth(img, img, cv.CV_BLUR, 3); 
            
            #convert the image to hsv(Hue, Saturation, Value) so its  
            #easier to determine the color to track(hue) 
            
            hsv_img = cv.CreateImage(cv.GetSize(img), 8, 3) 
            cv.CvtColor(img, hsv_img, cv.CV_BGR2HSV) 
            
            #limit all pixels that don't match our criteria, in this case we are  
            #looking for purple but if you want you can adjust the first value in  
            #both turples which is the hue range(120,140).  OpenCV uses 0-180 as  
            #a hue range for the HSV color model 
            
            #Orange  0-22
            #Yellow 22- 38
            #Green 38-75
            #Blue 75-130
            #Violet 130-160
            #Red 160-179
            
            thresholded_img =  cv.CreateImage(cv.GetSize(hsv_img), 8, 1) 
            cv.InRangeS(hsv_img, (0, 120, 120), (15, 255, 255), thresholded_img) 
            #cv.InRangeS(hsv_img, (120, 80, 80), (140, 255, 255), thresholded_img) 
            #determine the objects moments and check that the area is large  
            #enough to be our object 
            #moments = cv.Moments(thresholded_img, 0)
            moments = cv.Moments(cv.GetMat(thresholded_img),0) 
            area = cv.GetCentralMoment(moments, 0, 0) 
            
            #there can be noise in the video so ignore objects with small areas 
            if(area > 100000): 
                self.tracking = True
                self.lasttrack = time.time()
                #determine the x and y coordinates of the center of the object 
                #we are tracking by dividing the 1, 0 and 0, 1 moments by the area 
                x = cv.GetSpatialMoment(moments, 1, 0)/area 
                y = cv.GetSpatialMoment(moments, 0, 1)/area 
                
                #Write the x,y coords to a file for the pyFirmata code to use for controlling the Arduino
                f = open('values.txt',"w")
                f.write(str(x) + ":" + str(y))
                f.close()
                
                
                #create an overlay to mark the center of the tracked object 
                overlay = cv.CreateImage(cv.GetSize(img), 8, 3) 
                
                #cv.Circle(overlay, (x, y), 2, (255, 255, 255), 20) 
                cv.Circle(img, (int(x), int(y)), 2, (255, 255, 255), 20)
                cv.Add(img, overlay, img) 
                #add the thresholded image back to the img so we can see what was  
                #left after it was applied 
                cv.Merge(thresholded_img, None, None, None, img) 
            else:
                if self.tracking == True:
                    #We have just lost track of the object we need to hang around for a bit 
                    #to see if the object comes back.
                    f = open('values.txt','w')
                    f.write("-2:-2") #This tells the firmata script to stop moving the servos
                    f.close()
                    if time.time() >= self.lasttrack + self.hang_around_seconds:
                        self.tracking = False
                      
                if self.tracking == False:
                    f = open('values.txt',"w")
                    f.write("-1:-1")
                    f.close()
            #display the image  
            cv.ShowImage(color_tracker_window, img2) 
            
            if cv.WaitKey(10) == 27: 
                break 
                
if __name__=="__main__": 
    color_tracker = ColorTracker() 
    color_tracker.run() 