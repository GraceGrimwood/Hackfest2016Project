function initialize(curmap) {	
	console.log(curmap);
	var suburbPositions=[];
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
}