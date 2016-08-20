					$(document).ready(function() {

					// url to find latitude and longitude based on suburbs.
					var url="https://maps.googleapis.com/maps/api/geocode/json?address=Chertsey,NZ&key=AIzaSyB_g5IBb2LXiYkRRWnjZfLGivlXG-xZ-Fc";

					$.getJSON(url, function (response) {
						
						var latitude=response.results[0].geometry.location.lat;
						var longitude=response.results[0].geometry.location.lng;
						var place=new google.maps.LatLng(latitude,longitude);
						function initialize()
						{
						var mapProp = {
						  center:place,
						  zoom:7,
						  //mapTypeId:google.maps.MapTypeId.ROADMAP,
						  styles: [[{featureType:"administrative",
							elementType:"all",
							stylers:[{visibility:"on"}]
							},{
							featureType:"landscape",
							elementType:"all",
							stylers:[{hue:"#ff0300"},
									 {saturation:-100},
									 {lightness:129.33333333333334},
									 {gamma:1},
									 {visibility:"on"}]
							},{
							featureType:"poi",
							elementType:"all",
							stylers:[{hue:"#abff00"},
									 {saturation:61.80000000000001},
									 {lightness:13.800000000000011},
									 {gamma:1},
									 {visibility:"on"}]
							},{
							featureType:"road",
							elementType:"all",
							stylers:[{visibility:"off"}]
							},{
							featureType: "road.highway",
							elementType: "labels.icon",
							stylers: [{visibility: "off"}]
							},{
							featureType: "road.arterial",
							elementType: "all",
							stylers: [{hue: "#00b7ff"},
									  {saturation: -31.19999999999996},
									  {lightness: 2.1803921568627374},
									  {gamma: 1},
									  {visibility: "on"}]
							},{
							featureType: "road.local",
							elementType: "all",
							stylers: [{hue: "#00B5FF"},
									  {saturation: -33.33333333333343},
									  {lightness: 27.294117647058826},
									  {gamma: 1},
									  {visibility: "on"}]
							},{
							featureType:"transit.station.airport",
							elementType:"all",
							stylers:[{visibility:"on"}]
							},{
							featureType:"transit.station.bus",
							elementType:"all",
							stylers:[{visibility:"off"}]
							},{
							featureType:"water",
							elementType:"all",
							stylers:[{hue:"#00B7FF"},
									 {saturation:8.400000000000006},
									 {lightness:36.400000000000006},
									 {gamma:1}]}
							]]
						  };
						  
						var map = new google.maps.Map(document.getElementById("map"),mapProp);

						var myCity = new google.maps.Circle({
						  center:place,
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