import cv2
import time
import mediapipe as mp
import numpy as np
import HandTrackingModule as hm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


pTime =0
cTime =0

wCam,hCam = 640,480
cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

detector = hm.handDetector(detectionCon=0.7)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
rangeVol = volume.GetVolumeRange()
print(rangeVol)
minVol = rangeVol[0] 
maxVol = rangeVol[1] 
volBar = 400
per=0
while(True):
    success,img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img,draw=False)
   # print(lmList)

    if len(lmList)!=0:
        #print(lmList[4],lmList[8])
        x1,y1 = lmList[4][1],lmList[8][1]
        x2,y2 = lmList[4][2],lmList[8][2]
        cx,cy = (x1+y1)//2, (x2+y2)//2
        cv2.circle(img,(x1,x2),15,(255,0,255),cv2.FILLED)
        cv2.circle(img,(y1,y2),15,(255,0,255),cv2.FILLED)
        cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED)
        cv2.line(img,(x1,x2),(y1,y2),(255,0,0),3)
        length = math.hypot(y1-x1,y2-x2)
        print(length)

# hand 50 - 250
# volume -74 - 0

        vol = np.interp(length,[50,280],[minVol,maxVol])
        volBar = np.interp(length,[50,280],[400,150])
        per = np.interp(length,[50,280],[0,100])
        print(int(length) ,vol)
        volume.SetMasterVolumeLevel(vol, None)

        if length<50:
            cv2.circle(img,(cx,cy),15,(0,255,0),cv2.FILLED)

    cv2.rectangle(img,(50,150),(85,400),(0,255,0),3)   
    cv2.rectangle(img,(50,int(volBar)),(85,400),(0,255,0),cv2.FILLED)   
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime= cTime

    cv2.putText(img,f'fps : {(int(fps))}',(10,70),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3)
    cv2.putText(img,f'Volume : {(int(per))} %',(20,450),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3)

    cv2.imshow("Image",img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the camera and all resources
cap.release()
cv2.destroyAllWindows()

