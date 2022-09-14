import eel 
from fruit_ninja import run_ninja
from database2 import database
from os import remove 
from Socket import Connection
import random

@eel.expose
def say_something(word):
    if word[0] == "start":
        result = run_ninja()
        with open("temp.txt" , "w") as f:
            f.write(str(result))
        
        return result

    elif word[0] == "run":
        with open("temp.txt") as f:
            result = f.read()

        return result

    elif word[0] == "add":
        with open("temp.txt") as f:
            result = f.read()
        with open("temp2.txt" , "w") as f:
            f.write(word[1])

        database.add(word[1], float(result))

        return "recv!"
    
    elif word[0] == "board":
        with open("temp.txt") as f:
            result = f.read()
        with open("temp2.txt") as f:
            result2 = f.read()

        remove("temp.txt")
        remove("temp2.txt")
        
        
        user_list = (database.find(result),result2,result)
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
        result = run_ninja(id = id , database = database)
        
        
        with open("temp.txt" , "w") as f:
            f.write(str(result))
        
        database.remove(id)
        return result
    
    elif word[0] == "close":
        database.close(word[1])
        print("close")
        return True

database = database()

eel.init('web')

eel.start('start.html' , size = (800,600) , port=random.randint(7000,8000))