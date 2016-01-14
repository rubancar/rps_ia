function showUserHand(element) {
    var imgRock = document.getElementById("user_rock_hand");
    var imgPaper = document.getElementById("user_paper_hand");
    var imgScissors = document.getElementById("user_scissors_hand");

    if(element.getAttribute("data-section")=="user_rock_hand"){
        imgRock.setAttribute("class","show");
        imgPaper.setAttribute("class","hidden");
        imgScissors.setAttribute("class","hidden");
    }
    if(element.getAttribute("data-section")=="user_paper_hand"){
        imgRock.setAttribute("class","hidden");
        imgPaper.setAttribute("class","show");
        imgScissors.setAttribute("class","hidden");
    }
    if(element.getAttribute("data-section")=="user_scissors_hand"){
        imgRock.setAttribute("class","hidden");
        imgPaper.setAttribute("class","hidden");
        imgScissors.setAttribute("class","show");
    }
}

function addScore(element){
    var winS = document.getElementById("win_score");
    var tieS = document.getElementById("tie_score");
    var loseS = document.getElementById("lose_score");

    if(element=="win"){
        winS.innerHTML = parseInt(winS.innerHTML)+1;
    }
    if(element=="tie"){
        tieS.innerHTML = parseInt(tieS.innerHTML)+1;
    }
    if(element=="lose"){
        loseS.innerHTML = parseInt(loseS.innerHTML)+1;
    }
}

function resetScores(){
    document.getElementById("win_score").innerHTML=0;
    document.getElementById("tie_score").innerHTML=0;
    document.getElementById("lose_score").innerHTML=0;
}
