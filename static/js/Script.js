$(document).ready(function(){
            namespace = '/test'; // change to an empty string to use the global namespace

            // the socket.io documentation recommends sending an explicit package upon connection
            // this is specially important when using the global namespace
            socket = io.connect('http://' + document.domain + ':' + location.port + namespace);

            // event handler for server sent data
            // the data is displayed in the "Received" section of the page
            socket.on('my response', function(msg) {
                console.log(msg)
                //poner funcion msg.pc_jugada
                //$('#log').append('<br>' + $('<div/>').text('Usuario: ' + msg.user_jugada + ' PC: ' + msg.pc_jugada).html());
            });

            // event handler for new connections
            socket.on('connect', function() {
                socket.emit('my event', {data: 'I\'m connected!'});
            });

            $('form#piedra').submit(function(event) {
                socket.emit('piedra', {data: 'piedra'});
                return false;
            });

            $('form#papel').submit(function(event) {
                socket.emit('papel', {data: 'papel'});
                return false;
            });

            $('form#tijera').submit(function(event) {
                socket.emit('tijera', {data: 'tijera'});
                return false;
            });

            $('form#cadena').submit(function(event) {
                socket.emit('obtener cadena');
                return false;
            });

            $('form#reset').submit(function(event) {
                socket.emit('reset juego');
                return false;
            });

            $('form#disconnect').submit(function(event) {
                socket.emit('disconnect request');
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

        socket.emit('piedra', {data: 'piedra'});
        //return false;

    }
    if(element.getAttribute("data-section")=="user_paper_hand"){
        imgRock.setAttribute("class","hidden");
        imgPaper.setAttribute("class","show");
        imgScissors.setAttribute("class","hidden");
         socket.emit('papel', {data: 'papel'});

    }
    if(element.getAttribute("data-section")=="user_scissors_hand"){
        imgRock.setAttribute("class","hidden");
        imgPaper.setAttribute("class","hidden");
        imgScissors.setAttribute("class","show");
        socket.emit('tijera', {data: 'tijera'});

        
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

    socket.emit('reset juego');
}



