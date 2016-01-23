$(document).ready(function(){
    namespace = '/test'; // change to an empty string to use the global namespace
    socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
    socket.on('my response', function(msg) {
        console.log(msg.pc_jugada);        
        showPCHand(msg.pc_jugada);
        if(msg.user_jugada!=undefined) setScores(msg.user_jugada,msg.pc_jugada);
    });

    socket.on('arbol', function(msg) {
        console.log('nodos')
        console.log(msg.nodos)
        console.log('arcos')
        console.log(msg.arcos)
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


function showAlg(element){
    socket.emit('obtener arbol');
}

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
    if(user==pc){
        addScore("tie");
        showScoreMsg("tie");
    }
    jugada = user+pc;
    if(jugada=="PiedraTijera" || jugada=="TijeraPapel" || jugada=="PapelPiedra"){
        addScore("win");  
        showScoreMsg("win");
    } 
    if(jugada=="TijeraPiedra" || jugada=="PapelTijera" || jugada=="PiedraPapel"){
        addScore("lose");
        showScoreMsg("lose");
    }
}

function showScoreMsg(score){
    $("#win").attr("class","hidden");
    $("#tie").attr("class","hidden");
    $("#lose").attr("class","hidden");
    var seconds = 1700;
    switch(score){
        case "win":
            $("#win").attr("class","show");
            $("#win").fadeIn();
            $("#win").fadeOut(seconds);
            break;
        case "tie":
            $("#tie").attr("class","show");
            $("#tie").fadeIn();
            $("#tie").fadeOut(seconds);
            break;
        case "lose":
            $("#lose").attr("class","show");
            $("#lose").fadeIn();
            $("#lose").fadeOut(seconds);
            break;
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
    document.getElementById("user_rock_hand").setAttribute("class","show");
    document.getElementById("user_paper_hand").setAttribute("class","hidden");
    document.getElementById("user_scissors_hand").setAttribute("class","hidden");
    showPCHand("Piedra");
    socket.emit('reset juego');
}

$(function(){

    var cy = window.cy = cytoscape({
        container: document.getElementById('cy'),

boxSelectionEnabled: false,
autounselectify: true,

        layout: {
            name: 'dagre'
        },

        style: [
            {
                selector: 'node',
                style: {
                    'content': 'data(id)',
                    'text-opacity': 1,
                    'text-valign': 'center',
                    'text-halign': 'center',
                    'color': '#FFF',
                    'background-color': '#11479e'
                }
            },

            {
                selector: 'edge',
                style: {
                    'width': 4,
                    'target-arrow-shape': 'triangle',
                    'line-color': '#9dbaea',
                    'target-arrow-color': '#9dbaea'
                }
            }
        ],

        elements: {
            nodes: [
                { data: { id: 'n0' } },
                { data: { id: 'n1' } },
                { data: { id: 'n2' } },
                { data: { id: 'n3' } },
                { data: { id: 'n4' } },
                { data: { id: 'n5' } },
                { data: { id: 'n6' } },
                { data: { id: 'n7' } },
                { data: { id: 'n8' } },
                { data: { id: 'n9' } },
                { data: { id: 'n10' } },
                { data: { id: 'n11' } },
                { data: { id: 'n12' } },
                { data: { id: 'n13' } },
                { data: { id: 'n14' } },
                { data: { id: 'n15' } },
                { data: { id: 'n16' } }
            ],
            edges: [
                { data: { source: 'n0', target: 'n1' } },
                { data: { source: 'n1', target: 'n2' } },
                { data: { source: 'n1', target: 'n3' } },
                { data: { source: 'n4', target: 'n5' } },
                { data: { source: 'n4', target: 'n6' } },
                { data: { source: 'n6', target: 'n7' } },
                { data: { source: 'n6', target: 'n8' } },
                { data: { source: 'n8', target: 'n9' } },
                { data: { source: 'n8', target: 'n10' } },
                { data: { source: 'n11', target: 'n12' } },
                { data: { source: 'n12', target: 'n13' } },
                { data: { source: 'n13', target: 'n14' } },
                { data: { source: 'n13', target: 'n15' } },
            ]
        },
    });

});


