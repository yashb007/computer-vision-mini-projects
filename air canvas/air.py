import cv2
import numpy as np
from collections import deque


def setValues(a):
    print("")


cv2.namedWindow("Color detectors")
cv2.createTrackbar("Upper Hue", "Color detectors", 153, 180,setValues)
cv2.createTrackbar("Upper Saturation", "Color detectors", 255, 255,setValues)
cv2.createTrackbar("Upper Value", "Color detectors", 255, 255,setValues)
cv2.createTrackbar("Lower Hue", "Color detectors", 64, 180,setValues)
cv2.createTrackbar("Lower Saturation", "Color detectors", 72, 255,setValues)
cv2.createTrackbar("Lower Value", "Color detectors", 49, 255,setValues)



bpoints = [deque(maxlen=1024)]
gpoints = [deque(maxlen=1024)]
rpoints = [deque(maxlen=1024)]
ypoints = [deque(maxlen=1024)]

b_i=0
g_i=0
r_i=0
y_i=0

kernel = np.ones((5,5),np.uint8)

colors = [(255,0,0),(0,255,0),(0,0,255),(0,255,255)]
colorIndex = 0

#paint window
paintWin = np.zeros((471,636,3))+255
paintWin = cv2.rectangle(paintWin,(40,1),(140,65),(0,0,0),2)
paintWin = cv2.rectangle(paintWin,(160,1),(255,65),colors[0],-1)
paintWin = cv2.rectangle(paintWin,(275,1),(370,65),colors[1],-1)
paintWin = cv2.rectangle(paintWin,(390,1),(485,65),colors[2],-1)
paintWin = cv2.rectangle(paintWin,(505,1),(600,65),colors[3],-1)

cv2.putText(paintWin, "CLEAR", (49, 33), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
cv2.putText(paintWin, "BLUE", (185, 33), cv2.FONT_ITALIC, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paintWin, "GREEN", (298, 33), cv2.FONT_ITALIC, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paintWin, "RED", (420, 33), cv2.FONT_ITALIC, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paintWin, "YELLOW", (520, 33), cv2.FONT_ITALIC, 0.5, (150,150,150), 2, cv2.LINE_AA)
cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)

cap = cv2.VideoCapture(0)

while True:
    ret,frame = cap.read()
    frame = cv2.flip(frame,1)
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    u_hue = cv2.getTrackbarPos("Upper Hue", "Color detectors")
    u_saturation = cv2.getTrackbarPos("Upper Saturation", "Color detectors")
    u_value = cv2.getTrackbarPos("Upper Value", "Color detectors")
    l_hue = cv2.getTrackbarPos("Lower Hue", "Color detectors")
    l_saturation = cv2.getTrackbarPos("Lower Saturation", "Color detectors")
    l_value = cv2.getTrackbarPos("Lower Value", "Color detectors")
    Upper_hsv = np.array([u_hue,u_saturation,u_value])
    Lower_hsv = np.array([l_hue,l_saturation,l_value])

    frame = cv2.rectangle(frame, (40,1), (140,65), (122,122,122), -1)
    frame = cv2.rectangle(frame, (160,1), (255,65), colors[0], -1)
    frame = cv2.rectangle(frame, (275,1), (370,65), colors[1], -1)
    frame = cv2.rectangle(frame, (390,1), (485,65), colors[2], -1)
    frame = cv2.rectangle(frame, (505,1), (600,65), colors[3], -1)
    cv2.putText(frame, "CLEAR ALL", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150,150,150), 2, cv2.LINE_AA)

    Mask = cv2.inRange(hsv, Lower_hsv, Upper_hsv)
    Mask = cv2.erode(Mask, kernel, iterations=1)
    Mask = cv2.morphologyEx(Mask, cv2.MORPH_OPEN, kernel)
    Mask = cv2.dilate(Mask, kernel, iterations=1)

    _ , cnts , h = cv2.findContours(Mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE )
    center = None

    if len(cnts) > 0:
        # sorting the contours to find biggest contour
        cnt = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
        # Get the radius of the enclosing circle around the found contour
        ((x, y), radius) = cv2.minEnclosingCircle(cnt)
        # Draw the circle around the contour
        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
        # Calculating the center of the detected contour
        M = cv2.moments(cnt)
        center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
        if center[1] <= 65:
            if 40 <= center[0] <= 140: # Clear Button
                bpoints = [deque(maxlen=512)]
                gpoints = [deque(maxlen=512)]
                rpoints = [deque(maxlen=512)]
                ypoints = [deque(maxlen=512)]

                b_i = 0
                g_i = 0
                r_i = 0
                y_i = 0

                paintWin[67:,:,:] = 255
            elif 160 <= center[0] <= 255:
                    colorIndex = 0 # Blue
            elif 275 <= center[0] <= 370:
                    colorIndex = 1 # Green
            elif 390 <= center[0] <= 485:
                    colorIndex = 2 # Red
            elif 505 <= center[0] <= 600:
                    colorIndex = 3 # Yellow
        else :
            if colorIndex == 0:
                bpoints[b_i].appendleft(center)
            elif colorIndex == 1:
                gpoints[g_i].appendleft(center)
            elif colorIndex == 2:
                rpoints[r_i].appendleft(center)
            elif colorIndex == 3:
                ypoints[y_i].appendleft(center)
    else:
        bpoints.append(deque(maxlen=512))
        b_i += 1
        gpoints.append(deque(maxlen=512))
        g_i += 1
        rpoints.append(deque(maxlen=512))
        r_i += 1
        ypoints.append(deque(maxlen=512))
        y_i += 1

    points = [bpoints, gpoints, rpoints, ypoints]
    for i in range(len(points)):
        for j in range(len(points[i])):
            for k in range(1, len(points[i][j])):
                if points[i][j][k - 1] is None or points[i][j][k] is None:
                    continue
                cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 2)
                cv2.line(paintWin, points[i][j][k - 1], points[i][j][k], colors[i], 2)

    
    cv2.imshow("Tracking", frame)
    cv2.imshow("Paint", paintWin)
    cv2.imshow("mask",Mask)


    if cv2.waitKey(1) & 0xFF == ord("s"):
       print("enter the name of file") 
       file = input() 
       cv2.imwrite(file+".jpeg",paintWin)
       break;

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the camera and all resources
cap.release()
cv2.destroyAllWindows()