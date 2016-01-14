$(document).ready(function(){
    namespace = '/test'; // change to an empty string to use the global namespace

    // the socket.io documentation recommends sending an explicit package upon connection
    // this is specially important when using the global namespace
    socket = io.connect('http://' + document.domain + ':' + location.port + namespace);

    // event handler for server sent data
    // the data is displayed in the "Received" section of the page
    socket.on('my response', function(msg) {
        console.log(msg.pc_jugada);        
        showPCHand(msg.pc_jugada);
        //$('#log').append('<br>' + $('<div/>').text('Usuario: ' + msg.user_jugada + ' PC: ' + msg.pc_jugada).html());
        if(msg.user_jugada!=undefined) setScores(msg.user_jugada,msg.pc_jugada);
    });

    // event handler for new connections
    socket.on('connect', function() {
        socket.emit('my event', {data: 'I\'m connected!'});
    });

    $('form#cadena').submit(function(event) {
        socket.emit('obtener cadena');
        return false;
    });   
});


function showUserHand(element) {
    var imgRock = document.getElementById("user_rock_hand");
    var imgPaper = document.getElementById("user_paper_hand");
    var imgScissors = document.getElementById("user_scissors_hand");

    if(element.getAttribute("data-section")=="user_rock_hand"){
        imgRock.setAttribute("class","show");
        imgPaper.setAttribute("class","hidden");
        imgScissors.setAttribute("class","hidden");
        socket.emit('piedra', {data: 'Piedra'});
    }
    if(element.getAttribute("data-section")=="user_paper_hand"){
        imgRock.setAttribute("class","hidden");
        imgPaper.setAttribute("class","show");
        imgScissors.setAttribute("class","hidden");
         socket.emit('papel', {data: 'Papel'});
    }
    if(element.getAttribute("data-section")=="user_scissors_hand"){
        imgRock.setAttribute("class","hidden");
        imgPaper.setAttribute("class","hidden");
        imgScissors.setAttribute("class","show");
        socket.emit('tijera', {data: 'Tijera'});
    }
}

function showPCHand(element) {
    var imgRock = document.getElementById("pc_rock_hand");
    var imgPaper = document.getElementById("pc_paper_hand");
    var imgScissors = document.getElementById("pc_scissors_hand");

    if(element=="Piedra"){
        imgRock.setAttribute("class","show");
        imgPaper.setAttribute("class","hidden");
        imgScissors.setAttribute("class","hidden");        
    }
    if(element=="Papel"){
        imgRock.setAttribute("class","hidden");
        imgPaper.setAttribute("class","show");
        imgScissors.setAttribute("class","hidden");        
    }
    if(element=="Tijera"){
        imgRock.setAttribute("class","hidden");
        imgPaper.setAttribute("class","hidden");
        imgScissors.setAttribute("class","show");        
    }
}

function setScores(user,pc){    
    if(user==pc) addScore("tie");
    jugada = user+pc;
    if(jugada=="PiedraTijera" || jugada=="TijeraPapel" || jugada=="PapelPiedra") addScore("win");
    if(jugada=="TijeraPiedra" || jugada=="PapelTijera" || jugada=="PiedraPapel") addScore("lose");
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
    socket.emit('reset juego');
}



