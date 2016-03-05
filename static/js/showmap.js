"use strict";
var directionsDisplay;
var directionsService;
var map;
var totalDistance;
var marker;
var markers = [];
var hasMarkers = false;


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
$("#save-route-form").on("submit", saveRoute);




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

$("#save-run-form").on("submit", saveRun);


// POPULATE MAP WITH MARKERS/REMOVE MARKERS ON USER CLICK:

// 1. Functions to remove markers from map:
// Set the map to show all markers in the array.
function setMapToAllMarkers(map) {
  for (var i = 0; i < markers.length; i++) {
    markers[i].setMap(map);
  }
}

// Remove the markers from the map. Set hasMarkers to false
function clearMarkers() {
  setMapToAllMarkers(null);
  hasMarkers = false;
}


// 2. Function to add markers to the map:
// Define a marker for each latlng. Add it to the map, and to the marker array.
// Set hasMarkers to true
function makeMarkers(outages){
  // console.log(outages);

  for (var key in outages) {
      var outage = outages[key];

      marker = new google.maps.Marker({
          position: new google.maps.LatLng(outage.outage_lat, outage.outage_long),
          map: map,
          title: 'Marker ID: ' + key
      });
      markers.push(marker);
  }
  hasMarkers = true;
}


// Populate the map with markers if none are there; otherwise, remove markers from the map
function getData(evt){
  if (hasMarkers == false) {
      alert("you clicked the checkbox");
      $.get("/outages.json", makeMarkers);
      alert("processed get request");
  }
  else {
    alert("markers already present");
    clearMarkers();
  }
}
// call getDataFunction when user checks box
$("#show-streelight-form").on("change", getData);