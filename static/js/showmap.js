"use strict";
var directionsDisplay;
var directionsService;
var map;
var totalDistance;


function updateMap() {
  var startLat = $('#start-lat-field').data('startlat');
  var startLong = $('#start-long-field').data('startlong');

  var endLat = $('#end-lat-field').data('endlat');
  var endLong = $('#end-long-field').data('endlong');

   directionsService = new google.maps.DirectionsService();

   $("#right-panel").empty();
   map = new google.maps.Map(document.getElementById('map'), {
        zoom: 14,
        center: {lat: startLat, lng: startLong}, 
        styles: MAPSTYLES
    });

   directionsDisplay = new google.maps.DirectionsRenderer({
        draggable: true,
        map:map,
        panel: document.getElementById('right-panel')
    });

    directionsDisplay.addListener('directions_changed', function() {
        calculateTotalDistanceInKilometers(directionsDisplay.getDirections());
    });
    
    displayRoute({lat: startLat, lng: startLong }, {lat: endLat, lng: endLong }, directionsService, directionsDisplay)

}


function displayRoute(origin, destination, service, display){

    service.route({
      origin: origin,
      destination: destination,
      travelMode: google.maps.TravelMode.WALKING,
      avoidTolls: true
    }, function(response, status) {
      if (status === google.maps.DirectionsStatus.OK) {
        directionsDisplay.setDirections(response);  
        calculateTotalDistanceInKilometers(response);
        // console.log(response);  
      } else {
        alert('Could not display directions due to: ' + status);
      }
    });
}

//UTILITY METHOD TO CALC ROUTE DISTANCE IN KM
function calculateTotalDistanceInKilometers(response) {
  alert("calculateTotalDistanceInKilometers function called");
  console.log(response);  

  // get route data needed for db: total distance:
  totalDistance = 0;
  var currentRoute = response.routes[0];
  // for every leg of route, get the leg's distance, and add it to totalDistance
  for (var i = 0; i < currentRoute.legs.length; i++) {
    totalDistance += currentRoute.legs[i].distance.value;
  }
  //because distance.value contains value expressed in meters, convert meters to kilometers
  totalDistance = totalDistance/1000;
  alert("total km is " + totalDistance);
  //set the value of the total-distance field in the form

  // Hacking for now; can css later
  $("#total-distance-field1").val(totalDistance);
  $("#total-distance-field2").val(totalDistance);

}

