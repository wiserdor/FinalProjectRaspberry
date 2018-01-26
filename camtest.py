import io
import picamera
import cv2
import numpy
import time
import imutils
import json
import urllib.request
import threading
from picamera.array import PiRGBArray

url="http://52.214.218.83:3000/status"
data={}
stopCounter=0
startCounter=0
timeout=0

def sendJson(word):
    data['name']=word
    req = urllib.request.Request(url)
    req.add_header('Content-Type', 'application/json')
    jsondataasbytes = json.dumps(data).encode('utf-8')
    req.add_header('Content-Length', len(jsondataasbytes))
    response = urllib.request.urlopen(req, jsondataasbytes)


#Load a cascade file for detecting faces
handStop_cascade = cv2.CascadeClassifier('aGest.xml')
#Get the picture (low resolution, so it should be quite fast)
#Here you can also specify other parameters (e.g.:rotate the image)
camera=picamera.PiCamera()
camera.resolution = (320, 240)
#camera.rotation=180
camera.framerate=40
rawCapture = PiRGBArray(camera, size=tuple([320, 240]))
time.sleep(3);

for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    #Create a memory stream so photos doesn't need to be saved in a file
    frame = f.array
    

    #Now creates an OpenCV image
    image = cv2.imdecode(frame, 1)



    #Convert to grayscale
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    #Look for faces in the image using the loaded cascade file
    stopHands = handStop_cascade.detectMultiScale(gray, 1.1, 5)

    #increase hand counter
    if(len(stopHands)==1):
        stopCounter+=1
        print ("Found "+str(len(stopHands))+" stop Hand(s)")
    elif(len(stopHands)==2):
        startCounter+=1
        print ("Found "+str(len(stopHands))+" stop Hand(s)")
    else:
        stopCounter=0
        startCounter=0
        
    if(stopCounter==5):
        #call api
        print("Stop")
        stopCounter=0
        startCounter=0
        sendJson('stop')

        
    if(startCounter==5):
        #call api
        print("Start")
        stopCounter=0
        startCounter=0
        sendJson('start')
    #Draw a rectangle around every found face
    for (x,y,w,h) in stopHands:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),2)

    #Save the result image
    cv2.imshow('frame',frame)
    key = cv2.waitKey(1)
    rawCapture.truncate(0)
    if key == ord("q"):
       break        
