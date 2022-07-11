import cv2 
from cvzone.HandTrackingModule import HandDetector
import random 
import playsound
from time import time 
import threading

print("=== starting the device pls wait ===")


wCam , hCam = 1920 , 1080

cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FPS, 30)
cap.set(3 , wCam)
cap.set(4 , hCam)

detector = HandDetector( detectionCon=0.8 , minTrackCon=0.4,  maxHands=1)

marks = 0
playing = 0

x_pos , y_pos = random.randint(300,500) , 1000
end_time = time()+30

y_v = -1000
x_v = 100

fruits = [{"x_v" : 100 , "y_v" : -1000 , "x_pos" : random.randint(300,700) , "y_pos" : 1000 , "color" : (0,255,34) , "size" : 100 ,"name":"watermelon"} , 
{"x_v" : 100 , "y_v" : -1000 , "x_pos" : random.randint(300,700) , "y_pos" : 1000 , "color" : (255,0,0) , "size" : 60 , "name":"apple"},
{"x_v" : 100 , "y_v" : -1000 , "x_pos" : random.randint(300,700) , "y_pos" : 1000 , "color" : (0,0,0) , "size" : 75 , "name":"bomb"}]

def play_music(path):
    playsound.playsound(path, True)

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
                x1 , y1 = lmList[12][0] ,lmList[12][1]
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
                    marks = 0
                    
        else :
            if len(hands) > 0:
                lmList = hands[0]["lmList"]

                if len(lmList) > 5:
                    x1 , y1 = lmList[12][0] ,lmList[12][1]
                    cv2.circle(img , (x1 , y1) , 30 , (255,0,255) , cv2.FILLED)

                    for fruit in fruits:
                        if abs(x1-fruit["x_pos"]) < 50 and abs(y1-fruit["y_pos"]) < 50:
                            fruit["y_v"] = -1000
                            fruit["y_v"] = random.randint(-300,300)
                            fruit["x_pos"] , fruit["y_pos"] = random.randint(300,700) , 1000
                            
                            if fruit["name"] == "watermelon":
                                marks += 1
                                x = threading.Thread(target=play_music , args=["res/coin.mp3"])
                                x.start()

                            elif fruit["name"] == "apple":
                                marks += 2
                                x = threading.Thread(target=play_music , args=["res/coin.mp3"])
                                x.start()
                            else:
                                marks -= 3
                                x = threading.Thread(target=play_music , args=["res/bomb.mp3"])
                                x.start()

                            
            
            
            for fruit in fruits:

                if fruit["x_pos"] > 2000 or  fruit["y_pos"] > 1100 or fruit["x_pos"] < 0 or fruit["y_pos"] < 0 :
                    fruit["y_v"] = -1000
                    fruit["x_v"] = random.randint(-300,300)
                    fruit["x_pos"] , fruit["y_pos"] = random.randint(300,700) , 1000

    
                fruit["y_pos"] += int(fruit["y_v"] *(1/30))
                fruit["x_pos"] += int(fruit["x_v"] * (1/30))
                cv2.circle(img , (fruit["x_pos"],fruit["y_pos"]) , fruit["size"] , fruit["color"] , -1)
                fruit["y_v"] = fruit["y_v"] + 9.81 * 2

            cv2.putText(img , str(marks) , (50,50) , cv2.FONT_HERSHEY_SIMPLEX , 1, (255,0,0) , 2 ,  cv2.LINE_AA)
            cv2.putText(img , f"time remain : {remain_time}" , (1000,50) , cv2.FONT_HERSHEY_SIMPLEX , 1, (255,0,0) , 2 ,  cv2.LINE_AA)

    cv2.imshow("Img" , img)
    
    cv2.waitKey(1)