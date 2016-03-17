"use strict";
var directionsDisplay;
var directionsService;
var map;
var totalDistance;
var newRoute;
var waypoints;

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
        // everytime the directions change (including user dragging), update the polyline
        getPolyline(directionsDisplay.getDirections());
        getWaypoints(directionsDisplay.getDirections());
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
        // debugging: log the response object
        console.log(response.routes[0]);
        directionsDisplay.setDirections(response);  
        calculateTotalDistanceInKilometers(response);
      } else {
        alert('Could not display directions due to: ' + status);
      }
    });
}

//UTILITY METHOD TO CALC ROUTE DISTANCE IN KM
function calculateTotalDistanceInKilometers(response) { 

  // get route data needed for db: total distance:
  totalDistance = 0;
  var currentRoute = response.routes[0];
  // for every leg of route, get the leg's distance, and add it to totalDistance
  for (var i = 0; i < currentRoute.legs.length; i++) {
    totalDistance += currentRoute.legs[i].distance.value;
  }
  //because distance.value contains value expressed in meters, convert meters to kilometers
  totalDistance = totalDistance/1000;
  //set the value of the total-distance field in the form

  $("#total-distance-field1").val(totalDistance);
  $("#total-distance-field2").val(totalDistance);

}





function Route(name, polyline) {
  this.name = name;
  this.polyline = polyline;
}

Route.prototype.getName = function() {
  return this.name;
}


// GET THE POLYLINE FOR THE CURRENT ROUTE
function getPolyline(response) {
  var poly = response.routes[0]["overview_polyline"];
  // console.log(poly);
  // return poly;
  // newRoute = new Route("testName", poly);
  // console.log(newRoute);
  // console.log(newRoute.getName());
}

function getWaypoints(response) {
  var overviewPath = response.routes[0]["overview_path"];
  // console.log(overviewPath);
  waypoints = JSON.stringify(overviewPath);
  // console.log(JSON.stringify(overviewPath));
  // console.log(waypoints);

  // iterate over each latlng pair in overviewPath, convert it to a JSON representation
  // and add it to our waypoints array
  // for (var i = 0; i < overviewPath.length; i++) {
  //   var latlng = JSON.stringify(overviewPath[i]);
  //   console.log(latlng);
  //   waypoints.push(latlng);
  // }
  console.log(typeof(waypoints));
}


function recenterMap() {
  // var startLat = waypoints[1];
  // console.log(startLat.length);


  //  var dataArray = google.maps.Data.MultiPoint({lat:37.78083,lng:-122.4145});
  //  console.log(dataArray);
  //  directionsService = new google.maps.DirectionsService();

  //  $("#right-panel").empty();
  //  var map2 = new google.maps.Map(document.getElementById('map2'), {
  //       zoom: 14,
  //       center: {lat:37.78083,lng:-122.4145}, 
  //       styles: MAPSTYLES
  //   });


}


