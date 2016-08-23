function initialize(curmap) {	
	console.log(curmap);
	var suburbPositions=[];
<<<<<<< HEAD
	$.getJSON("/api/region/Ashburton/colourmap.json", function(data){
		
		suburbPositions=data;
		for(i=0;i<suburbPositions.length;i++){
			var myCity = new google.maps.Circle({
			  center:suburbPositions[i].center,
			  radius:2000,
			  strokeColor: rgbtohex(suburbPositions[i].Color),
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
	console.log(rgbval);
	var red = rgbval.split(",")[0];
	var green=rgbval.split(",")[1];
	var blue=rgbval.split(",")[2];
	return "#" +componenttohex(red) + componenttohex(green) + componenttohex(blue);
}

function componenttohex(c){
	var hex = c.toString(16);
	return hex.length===1 ? '0' + hex : hex;
=======
	$.getJSON("/api/regions/colourmap.json", function(data){
		suburbPositions=data;
		for(i=0;i<suburbPositions.length;i++){	
			for(j=0;j<suburbPositions[i].length;j++){
				var myCity = new google.maps.Circle({
					center:suburbPositions[i][j].center,
					radius:2000,
					strokeColor: suburbPositions[i][j].Color,
					strokeOpacity:0.3,
					strokeWeight:2,
					fillColor: suburbPositions[i][j].Color,
					fillOpacity:0.4
				});
				myCity.setMap(curmap);
			}
		}
	}); 
>>>>>>> master
}