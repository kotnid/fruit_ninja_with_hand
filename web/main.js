var results ;

async function start(){
    window.resizeTo(1, 1);
    result = await eel.say_something(['start'])();
    window.resizeTo(800, 600);
    
    var url = new URL(window.location.origin+"/end.html");
    console.log(result);
    url.searchParams.append("score", result);
    //url.searchParams.append("e_score", 5.5);
    console.log(url);
    location.href = url;
}

async function board(){
    console.log(window.location.href);
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const score = urlParams.get('score');
    const name = document.getElementById("fname").value;

    console.log(document.getElementById("fname").value);
    if (document.getElementById("fname").value != ""){
        result = await eel.say_something(['add',document.getElementById("fname").value, score])();
        var url = new URL(window.location.origin+"/board.html");

        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
        
        url.searchParams.append("score", score);
        url.searchParams.append("name", name);
        location.href = url;
    }else{
        alert("incorrect information , pls enter again!")
    }
    
}

async function run(){
    console.log(window.location.href);
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const score = urlParams.get('score');
    console.log(score);
   
    if (urlParams.has('e_score')){
        const e_score = urlParams.get('e_score');
        document.getElementById('score2').textContent = "Your enemy scored " + score +" marks!";
    }

    document.getElementById('score').textContent = "You scored " + e_score +" marks!";
    
}


async function back(){
    location.href = "start.html"
}

async function back2(){
    result = await eel.say_something(['close',num])();
    location.href = "start.html"
}

async function submit(){
    console.log("submit");
    var url = new URL(window.location.origin+"/board.html");

    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const score = urlParams.get('score');
    const name = urlParams.get('name');

    url.searchParams.append("score", score);
    url.searchParams.append("name", name);
    location.href = url;
}


async function result(){
    console.log(window.location.href);
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);

    results = await eel.say_something(['board',urlParams.get('score'),urlParams.get('name')])();
    
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
        if (i==0){
            new_row.className += " no1";
        }else if (i==1){
            new_row.className += " no2";
        }else if (i==2){
            new_row.className += " no3";
        }
        
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

        if (i==results.length-1){
            new_row.style = "background: #FFDAD6;color: #BA1A1A;";
            var table = document.getElementById("back");
            table.appendChild(new_row)
        }else{
            var table = document.getElementById("front");
            table.appendChild(new_row)
        }
        
    }
    
    
}

async function start2(){
    var num = prompt("Enter the num");
    //location.href = "test.html";
   
    results , enemy_result = await eel.say_something(['connect',num])();
    results2 = await eel.say_something(['close',num])();
    window.resizeTo(800, 600);

    var url = new URL(window.location.origin+"/end.html");
    url.searchParams.append("score", enemy_result[0]);
    url.searchParams.append("e_score", enemy_result[1]);
    console.log(url);
    alert(enemy_result[0]);
    alert(enemy_result[1]);
    // alert(results+" "+enemy_result);
    location.href = url;
}
