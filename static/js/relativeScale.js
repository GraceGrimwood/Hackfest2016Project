var medianSalesPrice;
// var population;
// var appreciation;
// var numberSales;

$.getJSON("http://localhost:8080/api/region/Auckland", 
    function (response) {
        //for each (resp in response){}
        var medianSalesPrice = response[2].MedianSalePrice;
    })


// $.getJSON( "ajax/test.json", function( data ) {
//   var items = [];
//   $.each( data, function( key, val ) {
//     items.push( "<li id='" + key + "'>" + val + "</li>" );
//   });
 
//   $( "<ul/>", {
//     "class": "my-new-list",
//     html: items.join( "" )
//   }).appendTo( "body" );
// });



var baseColor = [20,20,20];
var progressColor = [0,200,20];
var wholeColor = [200,50,60];
var progressMargin = 5;

function setup () {

    // in the js file:
    var MSPCanvas = createCanvas(250,15);
    MSPCanvas.parent("rs1");
    
}

function draw () {
    clear();
    baseBar();
    wholeBar();
    progressBar();
    // println(medianSalesPrice);
}

function baseBar(){
    push();
    noStroke();
    fill('#233142'); 
    rect(0,0, canvas.width, canvas.height, canvas.height);
    pop();
}

function progressBar(){
    push();
    noStroke();
    fill('#A7F76F'); 
    rect(progressMargin/2,progressMargin/2, canvas.width-50, canvas.height-progressMargin, canvas.height,0,0,canvas.height);
    pop();
}

function wholeBar(){
    push();
    noStroke();
    fill('#4A5872'); 
    rect(progressMargin/2,progressMargin/2, canvas.width-progressMargin, canvas.height-progressMargin, canvas.height,canvas.height,canvas.height,canvas.height);
    pop();
}

// median sales price

// population

// property appreciation 

// number of sales