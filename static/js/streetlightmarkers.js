var marker;
var markers = [];
var hasMarkers = false;
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