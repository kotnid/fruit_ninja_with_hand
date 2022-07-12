import eel 
from fruit_ninja import run_ninja
from os import remove 

@eel.expose
def say_something(word):
    if word == "start":
        result = run_ninja()
        with open("temp.txt" , "a") as f:
            f.write(str(result))
        
        return result

    elif word == "run":
        with open("temp.txt") as f:
            result = f.read()
        remove("temp.txt")
        return result

    elif word == "board":
        pass
        return "recv!"

eel.init('web')

eel.start('start.html' , size = (800,600))