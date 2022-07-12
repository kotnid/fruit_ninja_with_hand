async function start(){
    window.resizeTo(1, 1);
    result = await eel.say_something('start')();
    window.resizeTo(800, 600);
    location.href = "end.html"
}

async function board(){
    console.log("yo");
    result = await eel.say_something('board')()
    location.href = "board.html"
    console.log(result)
}

async function run(){
    result = await eel.say_something('run')();
    console.log(result);
    document.getElementById('score').textContent = "You scored " + result +" marks!"
}


async function back(){
    location.href = "start.html"
}

async function submit(){
    console.log("submit");
    location.href = "board.html"
}

