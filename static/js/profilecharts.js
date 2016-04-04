"use strict";


// #####################  Utility Method to Create Charts ###################################

function generateChart(url, renderingContext, lengendId) {
// Utility method: Get chart data via ajax. Use 2d rendering context to create the chart.

    $.get(url, function (data) {
        var lineChart = new Chart(renderingContext).Line(data, chartOptions);
        $("#" + lengendId).html(lineChart.generateLegend());
    });
}

// #################### Utility Method to Create Tables #########################################

// TODO


// ##################### Methods to Draw Charts and Tables #############################

var chartOptions = { responsive: true, scaleBeginAtZero: false };

// Get the 2d rendering context for canvas element ids lineChartDistance, lineChartPace
var ctxLineDistance = $("#lineChartDistance").get(0).getContext("2d");
var ctxLinePace = $("#lineChartPace").get(0).getContext("2d");

generateChart("/user-distance.json", ctxLineDistance, "lineLegendDistance");
generateChart("/user-pace.json", ctxLinePace, "lineLegendDistance");


// ################################################################################




// Create table with data on three most recently added routes

$( document ).ready(function() {
      $('#recent-routes-data-table').html("<tr><th>Course ID</th><th>Course Name</th><th>Date Added</th><th>Distance (km)</th></tr>");

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
      $('#recent-runs-data-table').html("<tr><th>Run ID</th><th>Course Name</th><th>Date of Run</th><th>Distance (km)</th><th>Duration</th></tr>");
      
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


