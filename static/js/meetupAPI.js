var key = "4d217e1b28e34774b426d215b563b7";
var meetupLong =2;
var meetupLat=3 ;
var meetupUrl = "https://api.meetup.com/find/groups?key="+key+"&sign=true&photo-host=public&lon="+meetupLong+"&lat="+meetupLat+"&page=20";


var oXHR = new XMLHttpRequest();

oXHR.open("GET", meetupUrl, true);

oXHR.onreadystatechange = function (oEvent) {  
    if (oXHR.readyState === 4) {  
        if (oXHR.status === 200) {  
          console.log(oXHR.responseText)  
        } else {  
           console.log("Error", oXHR.statusText);  
        }  
    }  
}; 

oXHR.send(null);  