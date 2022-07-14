import cv2 
from cvzone.HandTrackingModule import HandDetector
import random 
import playsound
from time import time 
import threading
import cvzone

def play_music(path):
    playsound.playsound(path, True)

def run_ninja():
    wCam , hCam = 1920 , 1080

    cap = cv2.VideoCapture(0 , cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(3 , wCam)
    cap.set(4 , hCam)

    detector = HandDetector( detectionCon=0.8 , minTrackCon=0.4,  maxHands=1)

    marks = 0

    x_pos , y_pos = random.randint(300,500) , 1000

    y_v = -1000
    x_v = 100

    multipler = 1

    fruits = [{"x_v" : 100 , "y_v" : -1000 , "x_pos" : random.randint(300,700) , "y_pos" : 1000 , "color" : (0,255,34) , "size" : 100 ,"name":"watermelon"} , 
    {"x_v" : 100 , "y_v" : -1000 , "x_pos" : random.randint(300,700) , "y_pos" : 1000 , "color" : (0,0,255) , "size" : 60 , "name":"apple"},
    {"x_v" : 100 , "y_v" : -1000 , "x_pos" : random.randint(300,700) , "y_pos" : 1000 , "color" : (0,0,0) , "size" : 75 , "name":"bomb"}]

    end_time = time() + 35

    while end_time - 30 > time():
        ret , img = cap.read()
        img = cv2.flip(img , 1)

        remain_time = int(end_time - 30 - time())

        cv2.putText(img , str(remain_time) , (800,500) , cv2.FONT_HERSHEY_SIMPLEX , 3 , (255,0,0) , 3 ,  cv2.LINE_AA)

        cv2.imshow("Img" , img)
        cv2.setWindowProperty("Img", cv2.WND_PROP_TOPMOST, 1)
        cv2.waitKey(1)

    while end_time > time():
        ret , img = cap.read()
        img = cv2.flip(img , 1)
        hands , img = detector.findHands(img)
    
        remain_time = int(end_time - time())
           
        if remain_time < 10:
            multipler = 1.5

        if len(hands) > 0:
            lmList = hands[0]["lmList"]

            if len(lmList) > 5:
                x1 , y1 = lmList[8][0] ,lmList[8][1]
                cv2.circle(img , (x1 , y1) , 30 , (255,0,255) , cv2.FILLED)

                for fruit in fruits:
                    if abs(x1-fruit["x_pos"]) < 70 and abs(y1-fruit["y_pos"]) < 70:
                        fruit["y_v"] = -1000
                        fruit["y_v"] = random.randint(-300,300)
                        fruit["x_pos"] , fruit["y_pos"] = random.randint(300,700) , 1000
                        
                        if fruit["name"] == "watermelon":
                            marks += 1 * multipler 
                            x = threading.Thread(target=play_music , args=["res/coin.mp3"])
                            x.start()

                        elif fruit["name"] == "apple":
                            marks += 2 * multipler 
                            x = threading.Thread(target=play_music , args=["res/coin.mp3"])
                            x.start()
                        else:
                            marks -= 3 * multipler 
                            x = threading.Thread(target=play_music , args=["res/bomb.mp3"])
                            x.start()
            
        for fruit in fruits:
            multipler2 = 1

            if multipler == 1.5:
                multipler2 = 1.2

            if fruit["x_pos"] > 2000 or  fruit["y_pos"] > 1100 or fruit["x_pos"] < 0 or fruit["y_pos"] < 0 :
                fruit["y_v"] = -1000 * multipler2
                fruit["x_v"] = random.randint(-300,300) 
                fruit["x_pos"] , fruit["y_pos"] = random.randint(400,800) , 1000


            fruit["y_pos"] += int(fruit["y_v"] *(1/30))
            fruit["x_pos"] += int(fruit["x_v"] * (1/30))
            cv2.circle(img , (fruit["x_pos"],fruit["y_pos"]) , fruit["size"] , fruit["color"] , -1)
            fruit["y_v"] = fruit["y_v"] + 9.81 * 2 * multipler

        cv2.putText(img , str(marks) , (50,50) , cv2.FONT_HERSHEY_SIMPLEX , 1, (255,0,0) , 2 ,  cv2.LINE_AA)
        cv2.putText(img , f"time remain : {remain_time}" , (1000,50) , cv2.FONT_HERSHEY_SIMPLEX , int(1* multipler) , (255,0,0) , 2 ,  cv2.LINE_AA)

        cv2.imshow("Img" , img)
        cv2.setWindowProperty("Img", cv2.WND_PROP_TOPMOST, 1)
        cv2.waitKey(1)
    
    cv2.destroyAllWindows()
    cap.release()
    
    return marks
 
if __name__ == "__main__":
    print("=== starting the device pls wait ===")
    run_ninja()