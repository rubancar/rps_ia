var renderer = new THREE.WebGLRenderer({alpha: true});
var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 1, 1000);
var result;
var stickFigure = {};

window.addEventListener('load', init, false);

function init() {
    renderer.setClearColor(0x000000, 1);
    renderer.setSize(window.innerWidth / 1.5 , window.innerHeight / 1.5);
    renderer.shadowMapEnabled = true;
    container = document.getElementById('render');
    container.appendChild(renderer.domElement);

    containerWidth = container.clientWidth;
    containerHeight = container.clientHeight;

    camera.position.x = 50;
    camera.position.y = 50;   
    camera.position.z = 300;    

    camera.lookAt(scene.position);
    scene.add(camera);

    //testCircle();

    var data = [[5.2,1],[5.7,2],[5,3],[4.2,4]];
    result = regression('linear', data);

    animate();
}

function animate() {
    requestAnimationFrame(animate);
    renderer.render(scene, camera);
}

function testCircle() {
    var centerX = 100;
    var centerY = 100;
    var radius = 40;

    var points = [];

    for (var degree = 0; degree < 360; degree++){
        var radians = degree * Math.PI/180;
        var x = centerX + radius * Math.cos(radians);
        var y = centerY + radius * Math.sin(radians);
        points.push({x: x,y: y});
    }

    var shape = recognizeStroke(points);
    if (shape) {
        scene.add(shape);
    }
}

function recognizeStroke(points) {

    var touchMoveX = [];
    var touchMoveY = [];

    points.forEach(function (point) {
        touchMoveX.push(point.x);
        touchMoveY.push(point.y);
    });

    var totalAmount = points.length;

    // sum up all coordinates and divide them by total length 
    // the average is a cheap approximation of the center.
    var averageX = touchMoveX.reduce( function ( previous, current) {
        return previous + current;
    } ) / totalAmount ;
    var averageY = touchMoveY.reduce( function ( previous, current) {
        return previous + current;
    } ) / totalAmount ;

    // compute distance to approximated center from each point
    var distances = touchMoveX.map ( function ( x, index ) {
        var y = touchMoveY[index];        
        return Math.sqrt( Math.pow(x - averageX, 2) + Math.pow(y - averageY, 2) );
    } );
    // average of those distance is 
    var averageDistance = distances.reduce ( function ( previous, current ) {
        return previous + current;
    } ) / distances.length;

    var min = averageDistance * 0.8;
    var max = averageDistance * 1.2;
    // filter out the ones not inside the min and max boundaries 
    var inRange = distances.filter ( function ( d ) {
       return d > min && d < max;
    } );

    var minPercentInRange = 80;
    var percentInRange = inRange.length / totalAmount * 100;
    // by the % of points within those boundaries we can guess if it's circle
    if ( !stickFigure.head && !stickFigure.body && percentInRange > minPercentInRange ) {
        console.log('Stroke is a head');
        var headDetails = {centroid: {x: averageX, y: averageY}, radius: averageDistance};
        stickFigure.head = headDetails;
        return drawCircle(headDetails.centroid, headDetails.radius);
    } else {
        console.log('Stroke is not recognized');
        return null;
    }
}

function drawCircle(centroid, radius) {
    var radius = radius,
    segments = 64,
    material = new THREE.LineBasicMaterial( { color: 0x0000ff } ),
    geometry = new THREE.CircleGeometry( radius, segments );

    // Remove center vertex
    geometry.vertices.shift();

    geometry.applyMatrix( new THREE.Matrix4().makeTranslation(centroid.x, centroid.y, 0) );
    //geometry.translate( centroid.x, centroid.y, 0 );

    return new THREE.Line( geometry, material );
}

function linearRegression(y,x){
		var lr = {};
		var n = y.length;
		var sum_x = 0;
		var sum_y = 0;
		var sum_xy = 0;
		var sum_xx = 0;
		var sum_yy = 0;
		
		for (var i = 0; i < y.length; i++) {
			
			sum_x += x[i];
			sum_y += y[i];
			sum_xy += (x[i]*y[i]);
			sum_xx += (x[i]*x[i]);
			sum_yy += (y[i]*y[i]);
		} 
		
		lr['slope'] = (n * sum_xy - sum_x * sum_y) / (n*sum_xx - sum_x * sum_x);
		lr['intercept'] = (sum_y - lr.slope * sum_x)/n;
		lr['r2'] = Math.pow((n*sum_xy - sum_x*sum_y)/Math.sqrt((n*sum_xx-sum_x*sum_x)*(n*sum_yy-sum_y*sum_y)),2);
		
		return lr;
}