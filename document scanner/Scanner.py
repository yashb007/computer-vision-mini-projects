import cv2
import numpy as np
import mapper


img = cv2.imread("test.jpg")
img=cv2.resize(img,(1300,800))
orig = img.copy()
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
blurr = cv2.GaussianBlur(gray,(5,5),0)
edged = cv2.Canny(blurr,30,50)
img,contours,hierarchy = cv2.findContours(edged,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours,key = cv2.contourArea,reverse=True)
target=[]
for c in contours:
    p=cv2.arcLength(c,True)
    approx = cv2.approxPolyDP(c,0.02*p,True)

    if len(approx)==4:
        target=approx
        break;
approx = mapper.mapp(target)
pts = np.float32([[0,0],[800,0],[800,800],[0,800]])
op = cv2.getPerspectiveTransform(approx,pts)
dst = cv2.warpPerspective(orig,op,(800,800))

while(True):
    cv2.imshow("Scanned",dst)
    if cv2.waitKey(1) & 0xFF == ord("q"):
                break
