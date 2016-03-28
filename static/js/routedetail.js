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
    console.log(response.start_address);

    
    var directionsTextArray = response.directions_text.split(",");
    console.log(directionsTextArray);

    var directionsDistanceArray = response.directions_distance.split(",");
    console.log(directionsDistanceArray);

    var summaryPanel = document.getElementById('right-panel');

    summaryPanel.innerHTML = '';
    summaryPanel.innerHTML += "<p>Walking directions are in beta. Use caution" 
    + " – This route may be missing sidewalks or pedestrian paths.<p>"
    summaryPanel.innerHTML += "Start Address: " + response.start_address + "</br>"
    // loop over directions array to populate each direction on new line
    var m;
    for (m = 0; m < directionsTextArray.length; m++) {
        summaryPanel.innerHTML += directionsTextArray[m];
        summaryPanel.innerHTML += "&nbsp &nbsp &nbsp &nbsp";

        summaryPanel.innerHTML += directionsDistanceArray[m];
        summaryPanel.innerHTML += "<br>";

    }
    summaryPanel.innerHTML += "End Address: " + response.end_address;
    summaryPanel.innerHTML += "<br>Map data ©2016 Google</br>";

}
