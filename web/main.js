async function start(){
    window.open('','_self').close()
    result = await eel.say_something('start')();
}

async function board(){
    result = await eel.say_something('board')()
    location.href = "board.html"
    console.log(result)
}

async function run(){
    console.log("start");
    result = await eel.say_something('run')();
    console.log(result);
    document.getElementById('score').textContent = result
}


async function back(){
    location.href = "start.html"
}

async function submit(){
    location.href = "board.html"
}