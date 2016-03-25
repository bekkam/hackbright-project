"use strict";

$.getJSON('all-run-data.json', function(data) {
      $.each(data, function(runId, ranRoute) {
            console.log(runId);
            console.log(ranRoute);
            var row = $("<tr />")
            $("#allRunsDataTable").append(row); 
            row.append($("<td>" + "<a href=" + "/runs/" + runId + ">"+ runId + "</td>"));
            row.append($("<td>" + ranRoute.route_name + "</td>"));
            row.append($("<td>" + ranRoute.run_date + "</td>"));
            row.append($("<td>" + ranRoute.route_distance + "</td>"));
            row.append($("<td>" + ranRoute.duration + "</td>"));
        });
});