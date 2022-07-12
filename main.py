import eel 
from fruit_ninja import run_ninja
from database import database
from os import remove 

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
        remove("temp.txt")

        database.add(word[1], float(result))

        return "recv!"
    
    elif word[0] == "board":
        return database.get()


database = database()

eel.init('web')

eel.start('start.html' , size = (800,600))