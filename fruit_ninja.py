import cv2 
from cvzone.HandTrackingModule import HandDetector
import random 
import playsound
from time import time 

print("=== starting the device pls wait ===")


wCam , hCam = 1920 , 1080

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 30)
cap.set(3 , wCam)
cap.set(4 , hCam)

detector = HandDetector( detectionCon=0.8 , minTrackCon=0.4,  maxHands=2)

marks = 0
playing = 0

x_pos , y_pos = random.randint(700,800) , random.randint(100,500)
end_time = time()+30

while True:
    ret , img = cap.read()
    img = cv2.flip(img , 1)
    hands , img = detector.findHands(img)

    if playing == 0 :
        cv2.putText(img , "Play fruit ninja" ,  (600,300) , cv2.FONT_HERSHEY_SIMPLEX , 1, (255,0,0) , 2 ,  cv2.LINE_AA)
        cv2.rectangle(img , (400,400) , (700,550) ,(255,0,0) , 2)
        
        if len(hands) > 0:
            lmList = hands[0]["lmList"]

            if len(lmList) > 5:
                x1 , y1 = lmList[8][0] ,lmList[8][1]
                cv2.circle(img , (x1 , y1) , 30 , (255,0,255) , cv2.FILLED)
                if (400 <= x1 <= 700) and (400 <= y1 <= 550):
                    playing = 1
                    end_time = time()+30

    elif playing == 1:
        
        remain_time = int(end_time - time())

        if remain_time < 0:
            cv2.putText(img , f"Your mark : {marks}" ,  (600,300) , cv2.FONT_HERSHEY_SIMPLEX , 1, (255,0,0) , 2 ,  cv2.LINE_AA)
            cv2.rectangle(img , (400,400) , (700,550) ,(255,0,0) , 2)

            if len(hands) > 0:
                lmList = hands[0]["lmList"]

            if len(lmList) > 5:
                x1 , y1 = lmList[8][0] ,lmList[8][1]
                cv2.circle(img , (x1 , y1) , 30 , (255,0,255) , cv2.FILLED)
                if (400 <= x1 <= 700) and (400 <= y1 <= 550):
                    playing = 0
                    
        else :
            if len(hands) > 0:
                lmList = hands[0]["lmList"]

                if len(lmList) > 5:
                    x1 , y1 = lmList[8][0] ,lmList[8][1]
                    cv2.circle(img , (x1 , y1) , 30 , (255,0,255) , cv2.FILLED)

                    if abs(x1-x_pos) < 20 and abs(y1-y_pos) < 20:
                        x_pos , y_pos = random.randint(400,800) , random.randint(100,500)
                        marks += 1 
                
                        playsound.playsound('res/coin.mp3', True)
            
            
            cv2.circle(img , (x_pos,y_pos) , 40 , (0,255,34) , -1)
            cv2.putText(img , str(marks) , (50,50) , cv2.FONT_HERSHEY_SIMPLEX , 1, (255,0,0) , 2 ,  cv2.LINE_AA)

            
            cv2.putText(img , f"time remain : {remain_time}" , (1000,50) , cv2.FONT_HERSHEY_SIMPLEX , 1, (255,0,0) , 2 ,  cv2.LINE_AA)

    cv2.imshow("Img" , img)
    
    cv2.waitKey(1)