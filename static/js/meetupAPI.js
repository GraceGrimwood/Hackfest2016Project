var key = "4d217e1b28e34774b426d215b563b7";
var lat =
var long = 
var url = "https://api.meetup.com/find/groups?key="+key+"&sign=true&photo-host=public&lon="+lon+"&lat="+lat+"&page=20";


	//Extracting state / country code info to get info from WUNDERGROUND API
	$.ajax({
		type:'GET',
	    url: url,
	    dataType: 'json',
	    success: function(meetup){
	    	console.log(meetup);

	    })
