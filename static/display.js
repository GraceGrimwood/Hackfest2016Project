function initMap() {
        var mapDiv = document.getElementById('map');
        var map = new google.maps.Map(mapDiv, {
            center: {lat: 44.540, lng: -78.546}, //This is how it focuses on a specific geo location. This is currently set to Sydney
            zoom: 8
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
			//Get the coordinates of the suburbs in a district --> Store in array --> Passed to HeatMapLayer
        });
      }