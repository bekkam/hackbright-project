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

}