import cv2
import os
import time
import HandTrackingModule as hm

wCam , hCam = 640,480
cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

pTime=0

myList = os.listdir("E:/computer vision/finger Counter/images")
print(myList)

overlay = []
for i in myList:
    image = cv2.imread("E:/computer vision/finger Counter/images/"+i)
    print("E:/computer vision/finger Counter/images/"+i)
    overlay.append(image)

print(len(overlay))

detector = hm.handDetector(detectionCon=0.75)
tipIds = [4,8,12,16,20]

while True:
    success,img = cap.read()
    img = detector.findHands(img)
    lmList= detector.findPosition(img,draw=False)

    if len(lmList)!=0:
        fList = []
        
        if lmList[tipIds[0]][1]<lmList[tipIds[0]-1][1]:
                fList.append(0)
        else:
                fList.append(1)

        for i in range(1,5):
            if lmList[tipIds[i]][2]<lmList[tipIds[i]-2][2]:
                fList.append(1)
            else:
                fList.append(0)
        fingerCount = fList.count(1)
        print(fingerCount)
        #print(fList)                
        h,w,c = overlay[fingerCount].shape

        img[0:h,0:w] = overlay[fingerCount]
        cv2.putText(img, str(int(fingerCount)), (45, 375), cv2.FONT_HERSHEY_PLAIN, 10,(255, 0, 0), 25)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    
    cv2.putText(img, str(int(fps)), (300, 70), cv2.FONT_HERSHEY_PLAIN, 3,(255, 0, 255), 3)
    cv2.imshow("Image",img)

    if cv2.waitKey(1) & 0xFF == ord("q"):
            break
