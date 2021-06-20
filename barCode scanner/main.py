import cv2
import numpy as np
from pyzbar.pyzbar import decode

cap = cv2.VideoCapture(0)
cap.set(4,480)
cap.set(3,640)

while True:
    suc,img = cap.read()
    decoded = decode(img)

    for code in decoded:
        print(code.data.decode('UTF-8'))
        pts = np.array([code.polygon],np.int32)
        pts = pts.reshape((-1,1,2))
        pts2=code.rect
        cv2.polylines(img,[pts],True,(255,0,0),5)
        cv2.putText(img,code.data.decode('UTF-8'),(pts2[0],pts2[ 1]),cv2.FONT_HERSHEY_SIMPLEX,0.9,(255,0,0),2)
    cv2.imshow("Result",img)
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
            break

