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
        center: {lat: startLat, lng: startLong} 
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



// SAVE A ROUTE ON USER CLICK
function showRouteResults(result){
  alert(result);
}

function saveRoute(evt){
  evt.preventDefault();

  var formInputs = {
    "route": $("#route-name").val(),

    "start_lat": $("#start-lat-field").val(),
    "start_long": $("#start-long-field").val(),
    "end_lat": $("#end-lat-field").val(),
    "end_long": $("#end-long-field").val(),

    "distance":$("#total-distance-field1").val(),
    "favorite":$("#favorite-field1").val()
  }; 
  $.post("/new-route", formInputs, showRouteResults);
}

function validateRouteForm(event){
  event.preventDefault();

  var charInput = $("#route-name").val().length;
  if (charInput < 2) {
    alert("Please enter at least two characters name for the Route");
  } else {
    saveRoute(event);
  }
}

$("#save-route-form").on("submit", validateRouteForm);




// SAVE A RUN ON USER CLICK
function showRunResults(result){
  alert(result);
}

function saveRun(evt){
  evt.preventDefault();

  var formInputs = {
    "route": $("#route-name2").val(),

    "start_lat": $("#start-lat-field").val(),
    "start_long": $("#start-long-field").val(),
    "end_lat": $("#end-lat-field").val(),
    "end_long": $("#end-long-field").val(),

    "distance":$("#total-distance-field2").val(),
    "favorite":$("#favorite-field2").val(),
    "date": $("#run-date-field").val(),
    "duration": $("#run-duration-field").val()
  }; 
  $.post("/new-run", formInputs, showRunResults);
}

// function validateRunForm(event){
//   event.preventDefault();

//   // var nameInput = $("#route-name").val().length;
//   var nameInput = $("#route-name").val().length;
//   var dateInput = $("#run-date-field").val().length;
//   var durationInput = $("#run-duration-field").val().length;
 
//   if (nameInput < 2) {
//     alert("Please enter at least two characters name for the Route");
//   } else {
//     saveRun(event);
//   }
// }

$("#save-run-form").on("submit", saveRun);

