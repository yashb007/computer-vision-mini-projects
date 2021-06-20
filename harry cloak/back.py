import cv2
import numpy as np
cap = cv2.VideoCapture(0)

while True:
    ret,frame = cap.read()

    if ret==False:
        continue
    cv2.imshow("frame",frame)
    key_pressed  = cv2.waitKey(5) & 0xFF
    if key_pressed==ord('q'):
        cv2.imwrite('img.jpeg',frame)
        break





cap.release()
cv2.destroyAllWindows()                 