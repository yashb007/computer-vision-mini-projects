import cv2
import numpy as np
cap = cv2.VideoCapture(0)
back= cv2.imread('./img.jpeg')
while True:
    ret,frame = cap.read()

    if ret==False:
        continue

    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)    

    #cv2.imshow("frame",hsv)
    red = np.uint8([[[0,0,255]]])
    hsv_red = cv2.cvtColor(red,cv2.COLOR_BGR2HSV)    
    #print(hsv_red)
    
    l_red = np.array([0,100,100])
    u_red = np.array([10,255,255])
    mask = cv2.inRange(hsv,l_red,u_red)
    #cv2.imshow("frame",mask)

    part1 = cv2.bitwise_and(back,back,mask=mask)

    mask = cv2.bitwise_not(mask)

    part2 = cv2.bitwise_and(frame,frame,mask=mask)

    cv2.imshow("part1",part1+part2)
    
    key_pressed  = cv2.waitKey(5) & 0xFF
    if key_pressed==ord('q'):
        #cv2.imwrite('img.jpeg',frame)
        break





cap.release()
cv2.destroyAllWindows()                 