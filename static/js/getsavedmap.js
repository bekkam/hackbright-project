"use strict";

function showSavedMap() {
  var startLat = $('#mapdata').data('getstartlat');
  var startLong = $('#mapdata').data('getstartlong');

  var endLat = $('#mapdata').data('getendlat');
  var endLong = $('#mapdata').data('getendlong');

  console.log("called showsavedmap function");
   var directionsDisplay = new google.maps.DirectionsRenderer();
   var directionsService = new google.maps.DirectionsService();

   var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 14,
    center: {lat: startLat, lng: startLong},
    styles: MAPSTYLES
  });


    directionsDisplay.setMap(map);
    directionsDisplay.setPanel(document.getElementById("right-panel"));

    directionsService.route({
      origin: {lat: startLat, lng: startLong} ,
      destination: {lat: endLat, lng: endLong} ,
      travelMode: google.maps.TravelMode.WALKING,
      avoidTolls: true
    }, function(response, status) {
      if (status === google.maps.DirectionsStatus.OK) {
        directionsDisplay.setDirections(response);  
      } else {
        alert('Could not display directions due to: ' + status);
      }
    });
}
