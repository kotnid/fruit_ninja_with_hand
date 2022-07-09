import cv2 
from cvzone.HandTrackingModule import HandDetector
import random 
import playsound

print("=== starting the device pls wait ===")

wCam , hCam = 1920 , 1080

cap = cv2.VideoCapture(0)
cap.set(3 , wCam)
cap.set(4 , hCam)

detector = HandDetector( detectionCon=0.8 , minTrackCon=0.4,  maxHands=2)

marks = 0
time = 30

x_pos , y_pos = random.randint(700,800) , random.randint(100,500)

while True:
    ret , img = cap.read()
    hands , img = detector.findHands(img)

    if len(hands) > 0:
        lmList = hands[0]["lmList"]

        if len(lmList) > 5:
            x1 , y1 = lmList[8][0] ,lmList[8][1]
            cv2.circle(img , (x1 , y1) , 30 , (255,0,255) , cv2.FILLED)

            if abs(x1-x_pos) < 20 and abs(y1-y_pos) < 20:
                x_pos , y_pos = random.randint(400,800) , random.randint(100,500)
                marks += 1 
                
                playsound.playsound('res/coin.mp3', True)
               

    cv2.circle(img , (x_pos,y_pos) , 20 , (255,255,0) , 20)
    cv2.putText(img , str(marks) , (50,50) , cv2.FONT_HERSHEY_SIMPLEX , 1, (255,0,0) , 2 ,  cv2.LINE_AA)
    cv2.putText(img , f"time remain : {time}" , (1000,50) , cv2.FONT_HERSHEY_SIMPLEX , 1, (255,0,0) , 2 ,  cv2.LINE_AA )
    cv2.imshow("Img" , img)
    
    cv2.waitKey(1)