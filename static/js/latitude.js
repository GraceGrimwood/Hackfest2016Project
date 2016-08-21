					//$(document).ready(function() {

					// url to find latitude and longitude based on suburbs.
						function initialize(map)
						{
						
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
					//});