var regions=[];
$(document).ready(function() {
	
	$.getJSON("/api/region/Hamilton", function(data){
	//console.log(data);
	
		$.each(data, function(i,item) {
			
			var url="https://maps.googleapis.com/maps/api/geocode/json?address="+item.Suburb+",NZ&key=AIzaSyB_g5IBb2LXiYkRRWnjZfLGivlXG-xZ-Fc";
			$.getJSON(url, function (response) {	
				var latitude=response.results[0].geometry.location.lat;
				var longitude=response.results[0].geometry.location.lng;
				var latlon=new google.maps.LatLng(latitude,longitude);
				regions.push({"name":item.Suburb,"center":latlon})
				//console.log(JSON.stringify());
			})
			
		})
		//console.log(regions);
	});
});