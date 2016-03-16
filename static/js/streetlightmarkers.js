var marker;
var markers = [];
var hasMarkers = false;
var heatmap;
var latLngs =[];
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
  // Make the query string for SODA API
  url = "https://data.sfgov.org/resource/vw6y-z8j6.json?"
    +"category=Streetlights"
    +"&Status=Open"

    // Get data, and add marker to lat/long on map
    $.getJSON(url, function(data) {
          $.each(data, function(i, entry) {
            // console.log(entry.point);
              var marker = new google.maps.Marker({
                  position: new google.maps.LatLng(entry.point.latitude, 
                                                   entry.point.longitude),
                  map: map,
                  title: entry.point.latitude + ", " + entry.point.longitude,
                  icon: {
                      path: google.maps.SymbolPath.BACKWARD_CLOSED_ARROW,
                      strokeColor: "navy",
                      scale: 3,
                      fillOpacity: 0.6
                  }
              });
              markers.push(marker);
          });
          hasMarkers = true;

    });
}


// Call makeMarkers if the map does not have markers; otherwise, remove markers from the map
function checkForMarkers(evt){
  if (hasMarkers == false) {
      makeMarkers();
  }
  else {
    clearMarkers();
  }
}
// call checkForMarkers when user checks box
$("#show-streelight-form").on("change", checkForMarkers);


function getLatLongs() {
  for (var i = 0; i < markers.length; i++) {
    latLngs.append(marker.position);
  }
  return latLngs;
}

function generateHeatMap() {
  alert("generateHeatMap called");
   heatmap = new google.maps.visualization.HeatmapLayer({
      data: getLatLongs(),
      map: map
    });

   heatmap.setMap(map);
}



$("#streetlight-data-heatmap").on("change", generateHeatMap);

