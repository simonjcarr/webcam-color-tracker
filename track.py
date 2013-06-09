#! /usr/bin/env python 

import cv 
import time


#TrackType
#Color = 1
#Faces = 2
TrackType = 2
class ColorTracker: 
    x = 0
    y = 0
    
    def __init__(self): 
        pass
        
        
    def runColor(self): 
        self.tracking = False
        self.lasttrack = None
        self.hang_around_seconds = 5
        color_tracker_window = "Preston HackSpace 2013 BarCamp Project" 
        cv.NamedWindow( color_tracker_window, 1 ) 
        self.capture = cv.CaptureFromCAM(0) 
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
                self.WriteXY(x, y)
                
                
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
                    self.WriteXY(-2, -2)
                    if time.time() >= self.lasttrack + self.hang_around_seconds:
                        self.tracking = False
                      
                if self.tracking == False:
                    self.WriteXY(-1, -1)
            #display the image  
            cv.ShowImage(color_tracker_window, img2) 
            
            if cv.WaitKey(10) == 27: 
                break 
    
    def WriteXY(self,X,Y):
        f = open('values.txt',"w")
        f.write(str(X) + ":" + str(Y))
        f.close()
            
    def runFaces(self):
        HAAR_CASCADE_PATH = "haarcascade_frontalface_default.xml"
        CAMERA_INDEX = 0
        cv.NamedWindow("Video", cv.CV_WINDOW_AUTOSIZE)
 
        capture = cv.CaptureFromCAM(CAMERA_INDEX)
        self.storage = cv.CreateMemStorage()
        self.cascade = cv.Load(HAAR_CASCADE_PATH)
        
        faces = []
     
        i = 0
        c = -1
        while (c == -1):
            image = cv.QueryFrame(capture)
    
            # Only run the Detection algorithm every 5 frames to improve performance
            #if i%5==0:
            faces = self.detect_faces(image)
            detected = 0
    
            for (x,y,w,h) in faces:
                detected = 1
                cv.Rectangle(image, (x,y), (x+w,y+h), 255)
                print x,y
                self.WriteXY(x,y)
            if detected == 0:
                self.WriteXY(-1, -1)
                
            cv.ShowImage("Video", image)
            i += 1
            c = cv.WaitKey(10)
            
        
    def detect_faces(self,image):
        faces = []
        detected = cv.HaarDetectObjects(image, self.cascade, self.storage, 1.2, 2, cv.CV_HAAR_DO_CANNY_PRUNING, (100,100))
        if detected:
            for (x,y,w,h),n in detected:
                faces.append((x,y,w,h))
        return faces
                
if __name__=="__main__": 
    color_tracker = ColorTracker() 
    color_tracker.runFaces() 