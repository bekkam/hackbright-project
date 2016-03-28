"use strict";

var pathname;

// function to get the last item from the url
function getLastItemInPath(path) {
    var urlArray = path.split("/");
    var lastItem = urlArray.pop();
    console.log(lastItem);
    return lastItem;
}

$( document ).ready(function() {
    pathname = window.location.pathname; // Returns path
    console.log(pathname);

    var id = getLastItemInPath(pathname);

    $.post("/route-detail.json", {routeId: id}, showIndividualRouteData);

});


function showIndividualRouteData(data) {
    // ##### new code
    console.log(data.waypoints);
    // ######
    $('#header').html("<h3>Route: " + data.route_name + "</h3>");
    $('#route-detail-data').html("<h4>Route Data</h4>");
    $("<tr><th>Route ID</th><th>Date Added</th><th>Distance (km)</th></tr></table>").appendTo('#route-detail-table');
    var row = $("<tr />");
    $("#route-detail-table").append(row); 
      row.append($("<td>" + data.route_id + "</td>"));
      row.append($("<td>" + data.add_date + "</td>"));
      row.append($("<td>" + data.route_distance + "</td>"));

    showSavedMap(data)
}

// TODO: Add function to populate run data table

// Add ability to generate map based on decoded polyline 

function showSavedMap(response) {

    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 14,
        center: {lat: response.waypoints[0][0], lng: response.waypoints[0][1]},
        styles: MAPSTYLES
    });

    var polyline = new google.maps.Polyline({
        path: [],
        strokeColor: 'green',
        strokeWeight: 4
    });

    // console.log(response.waypoints[0]);   
    var i;
    for (i = 0; i < response.waypoints.length; i++) {
        // console.log(response.waypoints[i]);
        // console.log(typeof(response.waypoints[i][0]));

        // FYI: Creating a latLng literal (line 70) did not work with google's API,
        // but creating a new LatLng did.  When functionality is missing, 
        // consider creating a new LatLng object instead.
        // polyline.getPath().push({lat: response.waypoints[i][0], lng: response.waypoints[i][1]})
        polyline.getPath().push(new google.maps.LatLng(response.waypoints[i][0], response.waypoints[i][1]));
    } 
    console.log("polyline is");
    console.log(polyline);
    polyline.setMap(map);


    console.log(response.directions_text);
    
    var directionsTextArray = response.directions_text.split(",");
    console.log(directionsTextArray);

    var directionsDistanceArray = response.directions_distance.split(",");
    console.log(directionsDistanceArray);

    var summaryPanel = document.getElementById('right-panel');

    summaryPanel.innerHTML = '';

    // loop over directions array to populate each direction on new line
    var m;
    for (m = 0; m < directionsTextArray.length; m++) {
        summaryPanel.innerHTML += directionsTextArray[m];
        summaryPanel.innerHTML += "&nbsp &nbsp &nbsp &nbsp";

        summaryPanel.innerHTML += directionsDistanceArray[m];
        summaryPanel.innerHTML += "<br>";

    }
    // summaryPanel.innerHTML += response.directions_text;
    // ############ new code to get directions #################

    // $.("#right-panel").html("hi");
    var directionsDisplay = new google.maps.DirectionsRenderer();
    var directionsService = new google.maps.DirectionsService();

    var lastWaypointIndex = response.waypoints.length -1;
    var originCoordinates = new google.maps.LatLng(response.waypoints[0][0], response.waypoints[0][1]);
    var destinationCoordinates = new google.maps.LatLng(response.waypoints[lastWaypointIndex][0], response.waypoints[lastWaypointIndex][1]);

    directionsDisplay.setMap(map);
    directionsDisplay.setPanel(document.getElementById("right-panel"));

    console.log("directionsService.route is");
    console.log(directionsService.route);
    directionsService.route({
      origin: originCoordinates ,
      destination: destinationCoordinates ,
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


        // console.log("response.directions_text is");
        // console.log(response.directions_text[0]);
        // var route = response.routes[0];
        // var summaryPanel = document.getElementById('right-panel');
        // summaryPanel.innerHTML = '';
        // // For each route, display summary information.
        // for (var i = 0; i < route.legs.length; i++) {
        //     var routeSegment = i + 1;
        //     summaryPanel.innerHTML += '<b>Route Segment: ' + routeSegment +
        //         '</b><br>';
        //     summaryPanel.innerHTML += route.legs[i].start_address + ' to ';
        //     summaryPanel.innerHTML += route.legs[i].end_address + '<br>';
        //     summaryPanel.innerHTML += route.legs[i].distance.text + '<br><br>';