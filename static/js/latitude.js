					$(document).ready(function() {

					// url to find latitude and longitude based on suburbs.
					var url="https://maps.googleapis.com/maps/api/geocode/json?address=Chertsey,NZ&key=AIzaSyB_g5IBb2LXiYkRRWnjZfLGivlXG-xZ-Fc";

					$.getJSON(url, function (response) {
						
						var latitude=response.results[0].geometry.location.lat;
						var longitude=response.results[0].geometry.location.lng;
						var amsterdam=new google.maps.LatLng(latitude,longitude);
						function initialize()
						{
						var mapProp = {
						  center:amsterdam,
						  zoom:7,
						  mapTypeId:google.maps.MapTypeId.ROADMAP
						  };
						  
						var map = new google.maps.Map(document.getElementById("map"),mapProp);

						var myCity = new google.maps.Circle({
						  center:amsterdam,
						  radius:20000,
						  strokeColor:"#0000FF",
						  strokeOpacity:0.8,
						  strokeWeight:2,
						  fillColor:"#0000FF",
						  fillOpacity:0.4
						  });

						myCity.setMap(map);
						}
						//google.maps.event.addDomListener(window, 'load', initialize);
						initialize();
					});
					});