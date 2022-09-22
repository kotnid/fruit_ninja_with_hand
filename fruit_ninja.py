import cv2 
from cvzone.HandTrackingModule import HandDetector
import random 
import playsound
import threading
import cvzone
import sched , time

def play_music(path):
    playsound.playsound(path, True)

def run_ninja(id=None , database = None):
    wCam , hCam = 1920 , 1080

    cap = cv2.VideoCapture(0 , cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(3 , wCam)
    cap.set(4 , hCam)

    detector = HandDetector( detectionCon=0.8 , minTrackCon=0.4,  maxHands=1)

    marks = 0

    s = sched.scheduler(time.time , time.sleep)

    global effect , spawn 

    multipler = 1
    effect = 1
    spawn = 1 

    
    fruits = [{"x_v" : random.randint(-300,300)  , "y_v" : -1000 , "x_pos" : random.randint(300,700) , "y_pos" : 1000 , "color" : (0,255,34) , "size" : 100 ,"name":"watermelon"} , 
    {"x_v" : random.randint(-300,300)  , "y_v" : -1000 , "x_pos" : random.randint(300,700) , "y_pos" : 1000 , "color" : (0,0,255) , "size" : 60 , "name":"apple"},
    {"x_v" : random.randint(-300,300)  , "y_v" : -1000 , "x_pos" : random.randint(300,700) , "y_pos" : 1000 , "color" : (0,0,0) , "size" : 75 , "name":"bomb"},
    {"x_v" : random.randint(-300,300)  , "y_v" : -1000 , "x_pos" : random.randint(300,700) , "y_pos" : 1000 , "color" : (255,255,0) , "size" : 70 , "name":"x2"}]

    end_time = time.time() + 33
    buffer_time = time.time()

    track_list_x = []
    track_list_y = []

    while end_time - 30 > time.time():
        ret , img = cap.read(cv2.IMREAD_UNCHANGED)
        img = cv2.flip(img , 1)

        remain_time = (end_time - 30 - time.time())

        # draw = ImageDraw.Draw(img)
        # draw.text((500, 400),  str(remain_time), font = font, fill = (255,0,0,0))
        # img = np.array(img)
        cv2.putText(img , str(round(remain_time,1)) , (int(img.shape[1]/2 - 250),int(img.shape[0]/2)) , cv2.FONT_HERSHEY_SIMPLEX , 5 , (132,91,90) , 7 ,  cv2.LINE_AA)

        cv2.imshow("Img" , img)
        cv2.setWindowProperty("Img", cv2.WND_PROP_TOPMOST, 1)
        cv2.waitKey(1)

    while end_time > time.time():
        ret , img = cap.read(cv2.IMREAD_UNCHANGED)
        img = cv2.flip(img , 1)
        hands , img = detector.findHands(img)
    
        remain_time = int(end_time - time.time())
        
        try:
            track_list_x.insert(0 , x1)
            track_list_y.insert(0 , y1)
        except:
            pass

        if len(track_list_x) > 20:
            track_list_x.pop()
            track_list_y.pop()

        for x in range(len(track_list_x)-1):
            cv2.line(img, (track_list_x[x] , track_list_y[x]), (track_list_x[x+1] , track_list_y[x+1]) , (255,0,255), len(track_list_x)-x)
            # cv2.circle(img , (track_list_x[x] , track_list_y[x]) , len(track_list_x)-x , (255,0,255) , cv2.FILLED)

        if remain_time < 10:
            multipler = 1.5

        if len(hands) > 0:
            lmList = hands[0]["lmList"]

            if len(lmList) > 5:
                x1 , y1 = lmList[8][0] ,lmList[8][1]

                track_list_x.insert(0 , x1)
                track_list_y.insert(0 , y1)

                if len(track_list_x) > 20:
                    track_list_x.pop()
                    track_list_y.pop()

                for x in range(len(track_list_x)-1):
                    cv2.line(img, (track_list_x[x] , track_list_y[x]), (track_list_x[x+1] , track_list_y[x+1]) , (255,0,255), len(track_list_x)-x)
                    # cv2.circle(img , (track_list_x[x] , track_list_y[x]) , len(track_list_x)-x , (255,0,255) , cv2.FILLED)

                cv2.circle(img , (x1 , y1) , 30 , (255,0,255) , cv2.FILLED)

                for fruit in fruits:
                    if abs(x1-fruit["x_pos"]) < 120 and abs(y1-fruit["y_pos"]) < 120:
                        fruit["y_v"] = -1000
                        fruit["y_v"] = random.randint(-300,300)
                        fruit["x_pos"] , fruit["y_pos"] = random.randint(300,700) , 1000
                        
                        if fruit["name"] == "watermelon":
                            marks += 1 * multipler * effect 
                            x = threading.Thread(target=play_music , args=["res/coin.mp3"])
                            x.start()

                        elif fruit["name"] == "apple":
                            marks += 2 * multipler * effect
                            x = threading.Thread(target=play_music , args=["res/coin.mp3"])
                            x.start()

                        elif fruit["name"] == "bomb":
                            marks -= 3 * multipler * effect
                            x = threading.Thread(target=play_music , args=["res/bomb.mp3"])
                            x.start()

                        elif fruit["name"] == "x2":
                            x = threading.Thread(target=play_music , args=["res/x2.mp3"])
                            x.start()

                            effect = 2 
                            spawn = 0
                            
                            def stop_x2():
                                global effect
                                effect = 1

                            def respawn():
                                global spawn
                                spawn = 1

                            def job():
                                s.enter(5 , 1,  stop_x2)
                                s.enter(random.randint(6 , 11) , 1 ,  respawn )
                                s.run()

                            threading.Thread(target=job).start()


        for fruit in fruits:
            if fruit["name"] == "x2" and spawn == 0 :
                continue

            multipler2 = 1

            if multipler == 1.5:
                multipler2 = 1.2

            if fruit["x_pos"] > 2200 or  fruit["y_pos"] > 1000 or fruit["x_pos"] < 0 or fruit["y_pos"] < 0 :
                fruit["y_v"] = -900 * multipler2
                fruit["x_v"] = random.randint(-300,300) 
                fruit["x_pos"] , fruit["y_pos"] = random.randint(400,800) , 900

                if fruit["name"] == "x2":
                     if fruit["x_pos"] > 2000 or  fruit["y_pos"] > 1100 or fruit["x_pos"] < 0 or fruit["y_pos"] < -100 :
                        spawn = 0

            fruit["y_pos"] += int(fruit["y_v"] *(1/30))
            fruit["x_pos"] += int(fruit["x_v"] * (1/30))
       
            #cv2.circle(img , (fruit["x_pos"],fruit["y_pos"]) , fruit["size"] , fruit["color"] , -1)
            fruit["y_v"] = fruit["y_v"] + 9.81 * 2 * multipler

            if fruit["name"] == "x2":
                s_img = cv2.imread("res/mango.png", -1)
                x_offset = fruit["x_pos"] - 75
                y_offset = fruit["y_pos"] - 59
                # text_size, _ = cv2.getTextSize("x2", cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
                # text_origin = (int(fruit["x_pos"] - text_size[0] // 2), int(fruit["y_pos"] + text_size[1] // 2))
                # cv2.putText(img , "x2" ,  text_origin , cv2.FONT_HERSHEY_SIMPLEX , 1, (255,0,0) , 2 ,  cv2.LINE_AA)

            elif fruit["name"] == "bomb":
                s_img = cv2.imread("res/bomb.png", -1)
                x_offset = fruit["x_pos"] - 81
                y_offset = fruit["y_pos"] - 88
                # text_size, _ = cv2.getTextSize("-3", cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
                # text_origin = (int(fruit["x_pos"] - text_size[0] // 2), int(fruit["y_pos"] + text_size[1] // 2))
                # cv2.putText(img , "-3" ,  text_origin , cv2.FONT_HERSHEY_SIMPLEX , 1, (255,0,0) , 2 ,  cv2.LINE_AA)
            
            elif fruit["name"] == "apple":
                s_img = cv2.imread("res/apple.png", -1)
                x_offset = fruit["x_pos"] - 88
                y_offset = fruit["y_pos"] - 88
                # text_size, _ = cv2.getTextSize("+2", cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
                # text_origin = (int(fruit["x_pos"] - text_size[0] // 2), int(fruit["y_pos"] + text_size[1] // 2))
                # cv2.putText(img , "+2" ,  text_origin , cv2.FONT_HERSHEY_SIMPLEX , 1, (255,0,0) , 2 ,  cv2.LINE_AA)

            elif fruit["name"] == "watermelon":
                s_img = cv2.imread("res/watermelon.png", -1)
                x_offset = fruit["x_pos"] - 100
                y_offset = fruit["y_pos"] - 100
                # text_size, _ = cv2.getTextSize("+1", cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
                # text_origin = (int(fruit["x_pos"] - text_size[0] // 2), int(fruit["y_pos"] + text_size[1] // 2))
                # cv2.putText(img , "+1" ,  text_origin , cv2.FONT_HERSHEY_SIMPLEX , 1, (255,0,0) , 2 ,  cv2.LINE_AA)

            if fruit["y_v"] > 0:
                s_img = cv2.rotate(s_img , cv2.ROTATE_180)

            y11, y12 = y_offset, y_offset + s_img.shape[0]
            x11, x12 = x_offset, x_offset + s_img.shape[1]

            alpha_s = s_img[:, :, 3] / 255.0
            alpha_l = 1.0 - alpha_s

            for c in range(0, 3):
                try:
                    img[y11:y12, x11:x12, c] = (alpha_s * s_img[:, :, c] +
                                        alpha_l * img[y11:y12, x11:x12, c])
                except:
                    pass
            
        

        cv2.line(img , (650,100), (img.shape[1]-300,100), (6,6,7), 6) 
        if remain_time < 10:
            cv2.putText(img , str(remain_time) , (650,70) , cv2.FONT_HERSHEY_SIMPLEX , 2 , (57,41,237) , 3 ,  cv2.LINE_AA)
            cv2.line(img , (650,100), (700+int((img.shape[1]-1000) * remain_time/30),100), (57,41,237), 5) 
        else:
            cv2.putText(img , str(remain_time) , (650,70) , cv2.FONT_HERSHEY_SIMPLEX , 2 , (132,91,90) , 3 ,  cv2.LINE_AA)
            cv2.line(img , (650,100), (700+int((img.shape[1]-1000) * remain_time/30),100), (132,91,90), 5) 

        num = 2

        if id != None:
            if buffer_time < time.time() :
                enermy_mark = database.update(float(marks),id)
                buffer_time = time.time()+1

            cv2.putText(img , f"enemy : " , (70,140) , cv2.FONT_HERSHEY_SIMPLEX , 2, (149,0,246) , 3 ,  cv2.LINE_AA)

            if (enermy_mark > marks):
                cv2.putText(img , str(enermy_mark) ,  (320,140) , cv2.FONT_HERSHEY_SIMPLEX ,2.5, (149,0,246) , 3 ,  cv2.LINE_AA)
                num = 2
            else :
                cv2.putText(img , str(enermy_mark) ,  (320,140) , cv2.FONT_HERSHEY_SIMPLEX , 2, (149,0,246) , 3 ,  cv2.LINE_AA)
                num = 2.5
        
        cv2.putText(img , "You : ", (70,70) , cv2.FONT_HERSHEY_SIMPLEX , 2, (149,0,246) , 3 ,  cv2.LINE_AA)
        cv2.putText(img , str(marks) ,  (280,70) , cv2.FONT_HERSHEY_SIMPLEX , num, (149,0,246) , 3 ,  cv2.LINE_AA)
        if effect == 2:
            cv2.putText(img , "x2" , (1100,200) , cv2.FONT_HERSHEY_SIMPLEX , 2, (57,41,237) , 3 ,  cv2.LINE_AA)

        cv2.imshow("Img" , img)
        cv2.setWindowProperty("Img", cv2.WND_PROP_TOPMOST, 1)
        cv2.waitKey(1)

    cv2.destroyAllWindows()
    cap.release()
    
    if id != None:
        return marks, enermy_mark

    return marks
 
if __name__ == "__main__":
    print("=== starting the device pls wait ===")
    run_ninja()