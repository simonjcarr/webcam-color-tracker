webcam-color-tracker
====================

This code was developed for the Preston HackSpace 2013 BarCamp stall in Blackpool

To run this code, you need the following installed

Python2.7
PySerial
PyFirmata

Instructions
Install PyFirmata Standard to an ArduinoMega

Attach the Arduino to the computer
Connect a Servo to Pin 7 (x axis - left and right)
Connect a Servo to pin 6 (y axis - up and down)

Install a WebCam and attach it to the servo horns (In what ever way you can, but make sure it is stable)

Run track.py - This will start the camera which will by default be looking for a green color.
Run firmata.py - This will start the connection to the Arduino.


More Detail.

track.py writes to the values.txt file the coords of the color it is tracking in relation to the webcam window.
firmata.py reads the values.txt file and trys to get the object into the center of the screen by moving the servo with the camera attached.


To Change the color alter the folloing line in track.py

cv.InRangeS(hsv_img, (38, 80, 80), (75, 255, 255), thresholded_img)

Alter the first number in each tuple based on the list below.
 	    Orange  0-22
            Yellow 22- 38
            Green 38-75
            Blue 75-130
            Violet 130-160
            Red 160-179

For more information on this google "openCV hue range for the HSV color model"

Have Fun!!!!
