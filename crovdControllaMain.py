# Import packages
import cv2
import time
from threading import Thread
import importlib.util
import paho.mqtt.client as mqtt        



class runCamera:
    def __init__(self,resolution=(640,480),framerate=30):
        self.stream = cv2.VideoCapture(0)
        ret = self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        ret = self.stream.set(3,resolution[0])
        ret = self.stream.set(4,resolution[1])
            
        (self.grabbed, self.frame) = self.stream.read()

        self.stopped = False

    def start(self):
        Thread(target=self.update,args=()).start()
        return self

    def update(self):
        while True:
            if self.stopped:
                self.stream.release()
                return

            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True

flag_connected = 0

def on_connect(client, userdata, flags, rc):
   global flag_connected
   flag_connected = 1

def on_disconnect(client, userdata, rc):
   global flag_connected
   flag_connected = 0
   


ourClient = mqtt.Client("peopleCOunter")     
ourClient.on_connect = on_connect
ourClient.on_disconnect = on_disconnect
ourClient.connect("test.mosquitto.org", 1883)  

ourClient.loop_start()



cam = runCamera(resolution=(640,480),framerate=30).start()

people_classifier=cv2.CascadeClassifier('Cascades/haarcascade_upperbody.xml')

count=0

while True:

    frame1=cam.read()
    
    height,width=frame1.shape[0:2]
    
    frame1[0:50,0:width]=[0,0,255]
    cv2.putText(frame1,'People count:',(5,30),cv2.FONT_HERSHEY_SIMPLEX,1.5,(255,255,255),2)
    
    cv2.line(frame1,(0,height-150),(width,height-150),(0,255,255),2)
    cv2.line(frame1,(0,height-50),(width,height-50),(0,100,255),2)
    
    blur=cv2.blur(frame1,(3,3))
    gray=cv2.cvtColor(blur,cv2.COLOR_BGR2GRAY)
    
    people=people_classifier.detectMultiScale(gray)
    
    for (x,y,w,h) in people:
        
        peopleCy=int(y+h/2)
        linIn=height-150
        linOut=height-50
        
        if(peopleCy<linIn+6 and peopleCy>linIn-6):
            if(count<3):
                count=count+1
                cv2.line(frame1,(0,height-150),(width,height-150),(0,0,255),5)
                if flag_connected==1:
                    ourClient.publish("subscribeTome", count);
        
        if(peopleCy<linOut+6 and peopleCy>linOut-6):
            if(count>0):
                count=count-1
                cv2.line(frame1,(0,height-50),(width,height-50),(0,0,255),5)
                if flag_connected==1:
                    ourClient.publish("subscribeTome", count);
        
        cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.putText(frame1,'Person',(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),2)
        cv2.putText(frame1,str(count),(500,30),cv2.FONT_HERSHEY_SIMPLEX,1.5,(255,255,255),2)

            
    cv2.imshow('CrovdControlla',frame1)
    key=cv2.waitKey(1)

    if cv2.waitKey(1) == ord('s'):
        break

# Clean up
cv2.destroyAllWindows()
videostream.stop()
