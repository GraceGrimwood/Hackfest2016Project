//var height = window.innerHeight

$(document).ready(function() {
 function setHeight() {
   windowHeight = $(window).innerHeight();
   $('#nav').css('height', windowHeight);
   $('#map').css('height', windowHeight);
 };
 setHeight();
 
 $(window).resize(function() {
   setHeight();
 });
});