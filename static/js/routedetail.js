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
    $('#header').html("<h3>Route: " + data.route_name + "</h3>");
    $('#route-detail-data').html("<h4>Route Data</h4>");
    $("<tr><th>Route ID</th><th>Date Added</th><th>Distance (km)</th></tr></table>").appendTo('#route-detail-table');
    var row = $("<tr />");
    $("#route-detail-table").append(row); 
      row.append($("<td>" + data.route_id + "</td>"));
      row.append($("<td>" + data.add_date + "</td>"));
      row.append($("<td>" + data.route_distance + "</td>"));
}

// TODO: Add function to populate run data table