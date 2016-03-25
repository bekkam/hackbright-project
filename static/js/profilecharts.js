"use strict";

// Charts 
// Line chart for user's run distance over time
var options = {
  responsive: true,
  scaleBeginAtZero: false
};
var ctxLineDistance = $("#lineChartDistance").get(0).getContext("2d");

$.get("/user-distance.json", function (data) {
  var lineChartUserDistance = new Chart(ctxLineDistance).Line(data, options);
  $("#lineLegendDistance").html(lineChartUserDistance.generateLegend());
});

// Line chart for user's running pace over time
var options = {
  responsive: true,
  scaleBeginAtZero: false
};
var ctxLinePace = $("#lineChartPace").get(0).getContext("2d");

$.get("/user-pace.json", function (data) {
  var lineChartUserPace = new Chart(ctxLinePace).Line(data, options);
  $("#lineLegendPace").html(lineChartUserPace.generateLegend());
});


// Create table with data on three most recently added routes

$( document ).ready(function() {
      $('#recent-routes-data-table').html("<tr><th>Route ID</th><th>Route Name</th><th>Date Added</th><th>Distance (km)</th></tr>");

      $.getJSON('/three-recent-routes.json', function(data) {
            $.each(data, function(id, route) {
                  var row = $("<tr />");
                  $("#recent-routes-data-table").append(row); 
                  row.append($("<td>" + id + "</td>"));
                  row.append($("<td>" + "<a href=" + "/routes/" + id + ">" + route.route_name + "</td>"));
                  row.append($("<td>" + route.add_date + "</td>"));
                  row.append($("<td>" + route.route_distance + "</td>"));
              });
      });
});

// Create table with data on three most recent runs

$( document ).ready(function() {
      $('#recent-runs-data-table').html("<tr><th>Run ID</th><th>Route Name</th><th>Date of Run</th><th>Distance (km)</th><th>Duration</th></tr>");
      
      $.getJSON('/three-recent-runs.json', function(data) {
            $.each(data, function(runId, ranRoute) {
                  var row = $("<tr />");
                  $("#recent-runs-data-table").append(row); 
                  row.append($("<td>" + "<a href=" + "/runs/" + runId + ">"+ runId + "</td>"));
                  row.append($("<td>" + ranRoute.route_name + "</td>"));
                  row.append($("<td>" + ranRoute.run_date + "</td>"));
                  row.append($("<td>" + ranRoute.route_distance + "</td>"));
                  row.append($("<td>" + ranRoute.duration + "</td>"));
              });
      });
});
