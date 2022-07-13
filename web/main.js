async function start(){
    window.resizeTo(1, 1);
    result = await eel.say_something(['start'])();
    window.resizeTo(800, 600);
    location.href = "end.html"
}

async function board(){
    console.log(document.getElementById("fname").value);
    if (document.getElementById("fname").value != ""){
        location.href = "board.html"
        result = await eel.say_something(['add',document.getElementById("fname").value])()
    }else{
        alert("incorrect information , pls enter again!")
    }
    
}

async function run(){
    result = await eel.say_something(['run'])();
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


async function result(){
    results = await eel.say_something(['board'])();
    
    for (let i=0 ; i <= results.length-1 ; i++){
        console.log(i)
        if  (i == results.length-1){
            console.log(results[i][0])
            rank = results[i][0]
            user = results[i][1]
            score = results[i][2]
        } else{
            rank = i + 1 
            user = results[i][0]
            score = results[i][1]
        }
         
        var new_row = document.createElement('div');
        new_row.className = "header"
        
        var new_rank = document.createElement('div');
        new_rank.className = "left"
        new_rank.textContent = rank
        new_row.appendChild(new_rank)

        var new_user = document.createElement('div');
        new_user.className = "center"
        new_user.textContent = user
        new_row.appendChild(new_user)

        var new_score = document.createElement('div');
        new_score.className = "right"
        new_score.textContent = score
        new_row.appendChild(new_score)

        var table = document.getElementById("put");
        table.appendChild(new_row)
        console.log("run jor");
    }
    
    
}