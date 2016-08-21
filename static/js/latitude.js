function initialize(map) {	
	console.log(map);
	var suburbPositions=[];
	$.getJSON("/static/js/SuburbsLatlon.json", function(data){
		suburbPositions=data;
		for(i=0;i<suburbPositions.length;i++){	
			var myCity = new google.maps.Circle({
			  center:suburbPositions[i].center,
			  radius:2000,
			  strokeColor:"#0000FF",
			  strokeOpacity:0.3,
			  strokeWeight:2,
			  fillColor:"#0000FF",
			  fillOpacity:0.4
			});
		
			myCity.setMap(map);
		}
	}); 
}

function rgbtohex(rgbval){
	red = rgbval.split(",")[0];
	green=rgbval.split(",")[1];
	blue=rgbval.split(",")[2];
	return "#" +componenttohex(red) + componenttohex(green) + componenttohex(blue);
}

function componenttohex(c){
	var hex = c.toString(16);
	return hex.length===1 ? '0' + hex : hex;
	
	
	
}