import eel 
from fruit_ninja import run_ninja
from database import database
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

        user_list = (database.find(result)[0],result2,result)
        data_list = database.get()
        data_list.append(user_list)
        print(data_list)
        return data_list

    elif word[0] == "connect":
        app = Connection()
        print("finish running")
        result = run_ninja(app)
        app.end()
        with open("temp.txt" , "w") as f:
            f.write(str(result))
        
        return result

database = database()

eel.init('web')

eel.start('start.html' , size = (800,600) , port=random.randint(7000,8000))