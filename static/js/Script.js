$(document).ready(function(){
    namespace = '/test'; // change to an empty string to use the global namespace
    socket = io.connect('http://' + document.domain + ':' + location.port + namespace);    
    socket.on('my response', function(msg) {
        console.log(msg.pc_jugada);        
        showPCHand(msg.pc_jugada);
        if(msg.user_jugada!=undefined) setScores(msg.user_jugada,msg.pc_jugada);
    });

    socket.on('dibujar arbol', function(msg) {        
        arbol = msg
        console.log("mi jugada:"+msg.mi_jugada)
        console.log("prediccion"+msg.prediccion)
        console.log(msg.estrategia)
        showMap();
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

function createTree(){
    cyJson = 
    {
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
                    'background-color': '#727272',
                    'width': 125,
                    'label': "data(label)"
                }
            },
            {
                selector: 'edge',
                style: {
                    'width': 2,
                    'target-arrow-shape': 'triangle',
                    'line-color': '#B6B6B6',
                    'target-arrow-color': '#B6B6B6'
                }
            }
        ],
        elements: {
            nodes: [ ],
            edges: [ ]
        },
    }
    var nodes = arbol.nodos;
    var edges = arbol.arcos;
    //Add nodes
    for(i=0; i<nodes.length; i++){
        cyJson["elements"]["nodes"].push({data: { id: nodes[i][0], label: 'R:'+nodes[i][1]+' S:'+nodes[i][2]+' P:'+nodes[i][3] }});
    }

    //Add edges
    for(i=0; i<edges.length; i++){
        cyJson["elements"]["edges"].push({data: { source: edges[i][0], target: edges[i][1]}});
    }

    var cy = window.cy = cytoscape(cyJson);
}

function pcThinking(){
    socket.emit('obtener arbol');
}

function showMap(){    
    createTree();
    $("#cy").attr("class","showCanvas"); 
    treePng = cy.png({ full: true, maxHeight:400, maxWidth:500});
    $("#imgTree").attr("src",treePng);
    $("#cy").attr("class","hidden");
}

function createPopup(){
    var popup, popupBody, bodySection, title, subtitle, members, inst;

    popup = document.createElement("div");
    popup.setAttribute("class", "pop");

    popupBody = document.createElement("div");
    popupBody.setAttribute("class","popBody");

    title = document.createElement("h2");
    title.innerHTML = "Rock, Paper, Scissors";
    popupBody.appendChild(title);

    members = document.createElement("p");
    var t = document.createTextNode("Choose the algorithm you want the computer to implement:")
    members.appendChild(t);
    popupBody.appendChild(members);

    var div = document.createElement("div");
    var pathsTree = document.createElement("input");
    pathsTree.setAttribute("id","pathsTree");
    pathsTree.setAttribute("type","submit");
    pathsTree.setAttribute("value","Paths Tree");
    pathsTree.addEventListener("click",empezarClicked,false);
    div.appendChild(pathsTree);
    popupBody.appendChild(div);

    var div = document.createElement("div");
    var gA = document.createElement("input");
    gA.setAttribute("id","gA");
    gA.setAttribute("type","submit");
    gA.setAttribute("value","Genetic Algorithm");
    gA.addEventListener("click",empezarClicked,false);
    div.appendChild(gA);
    popupBody.appendChild(div);

    popup.appendChild(popupBody);

    bodySection = document.body;
    bodySection.appendChild(popup);
}

function empezarClicked(event){
    chosenAlg = event.target.value;
    cerrarPopup();
}

function cerrarPopup(){
    var popup = document.getElementsByClassName("pop")[0];
    document.body.removeChild(popup);
}