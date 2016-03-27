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

    $.post("/run-detail.json", {runId: id}, showRunData);

});


function showRunData(data) {
    $('#run-header').html("<h3>Run ID:" + data.run_id + "</h3>");
    $('#run-detail-data').html("<h4>Run Data</h4>");
    $("<tr><th>Route Name</th><th>Date of Run</th><th>Distance (km)</th><th>Duration</th></tr>").appendTo('#run-detail-table');
    var row = $("<tr />");
    $("#run-detail-table").append(row); 
      row.append($("<td>" + data.route_name + "</td>"));
      row.append($("<td>" + data.run_date + "</td>"));
      row.append($("<td>" + data.route_distance + "</td>"));
      row.append($("<td>" + data.duration + "</td>"));
    
    showSavedMap(data);
}

// Add ability to gdenerate map based on decoded polyline 

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

    console.log(response.waypoints[0]);   
    var i;
    for (i = 0; i < response.waypoints.length; i++) {
        console.log(response.waypoints[i]);
        console.log(typeof(response.waypoints[i][0]));

        // polyline.getPath().push({lat: response.waypoints[i][0], lng: response.waypoints[i][1]})
        polyline.getPath().push(new google.maps.LatLng(response.waypoints[i][0], response.waypoints[i][1]));
    } 
    console.log("polyline is");
    console.log(polyline);
    polyline.setMap(map);

}