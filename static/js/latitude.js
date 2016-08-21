$(document).ready(function() {
	var suburbPositions=[];
	$.getJSON("/static/js/SuburbsLatlon.json", function(data){
		suburbPositions=data;
		initialize(suburbPositions);
	});
});	
function initialize(suburbLatLngs) {	
	var mapProp = {
		center:suburbLatLngs[0].center,
		zoom:7,
		mapTypeId:google.maps.MapTypeId.ROADMAP
	};  
	var map = new google.maps.Map(document.getElementById("googleMap"),mapProp);
	for(i=0;i<suburbLatLngs.length;i++){	
		var myCity = new google.maps.Circle({
		  center:suburbLatLngs[i].center,
		  radius:3000,
		  strokeColor:"#0000FF",
		  strokeOpacity:0.3,
		  strokeWeight:2,
		  fillColor:"#0000FF",
		  fillOpacity:0.4
		});
	
		myCity.setMap(map);
	}
}
	
	

