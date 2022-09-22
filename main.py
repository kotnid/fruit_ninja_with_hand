import eel 
from fruit_ninja import run_ninja
from database2 import database
from os import remove 

@eel.expose
def say_something(word):
    if word[0] == "start":
        result = run_ninja()
             
        return result

    elif word[0] == "add":
        database.add(word[1], word[2])

        return "recv!"
    
    elif word[0] == "board": 
        user_list = (database.find(word[1]),word[2],word[1])
        data_list2 = database.get()
        data_list = []

        for doc in data_list2:
            doc = doc.to_dict()
            data_list.append((doc['name'] , doc['score']))

        data_list.append(user_list)
        #print(data_list) 
        return data_list

    elif word[0] == "connect":
        print(word[1])
        id = database.search(word[1])
        result,enemy_result = run_ninja(id = id , database = database)

        database.remove(id)
        return result,enemy_result
    
    elif word[0] == "close":
        database.close(word[1])
        print("close")
        return True

database = database()

eel.init('web')

eel.start('start.html' , size = (800,600))