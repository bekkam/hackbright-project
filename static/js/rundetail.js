"use strict";

// function to get the last item from the url
function getLastItemInPath(path) {

    var urlArray = path.split("/");
    var lastItem = urlArray.pop();
    console.log(lastItem);
    return lastItem;
}

$( document ).ready(function() {

    var id = getLastItemInPath(window.location.pathname);
    $.post("/run-detail.json", {runId: id}, showRunData);
});


function showRunData(data) {

    $('#run-header').html("<h3>Run ID:" + data.run_id + "</h3>");
    $('#run-detail-data').html("<h4>Run Data</h4>");
    $("<tr><th>Course Name</th><th>Date of Run</th><th>Distance (km)</th><th>Duration</th></tr>").appendTo('#run-detail-table');
    var row = $("<tr />");
    $("#run-detail-table").append(row); 
      row.append($("<td>" + data.course_name + "</td>"));
      row.append($("<td>" + data.run_date + "</td>"));
      row.append($("<td>" + data.course_distance + "</td>"));
      row.append($("<td>" + data.duration + "</td>"));
    
    showSavedRunMap(data);
}


// #################### Render a map and custom polyline ########################3
function showSavedRunMap(response) {

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

    var bounds = new google.maps.LatLngBounds();

    var i;
    for (i = 0; i < response.waypoints.length; i++) {

        // FYI: Creating a latLng literal (line 70) did not work with google's API,
        // but creating a new LatLng did.  When functionality is missing, 
        // consider creating a new LatLng object instead.
        // polyline.getPath().push({lat: response.waypoints[i][0], lng: response.waypoints[i][1]})
        polyline.getPath().push(new google.maps.LatLng(response.waypoints[i][0], response.waypoints[i][1]));
        bounds.extend(new google.maps.LatLng(response.waypoints[i][0], response.waypoints[i][1]));
    } 

    polyline.setMap(map);
    map.fitBounds(bounds)
    showRunDirections(response);
}

// ########################## Render custom directions for the polyline ###############
function showRunDirections(response) {
    
    var directionsTextArray = response.directions_text.split(",");
    var directionsDistanceArray = response.directions_distance.split(",");

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
