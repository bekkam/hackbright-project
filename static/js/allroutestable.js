"use strict";

$( document ).ready(function() {
      $('#allRoutesDataTable').html("<tr><th>Route ID</th><th>Route Name</th><th>Date Added</th><th>Distance (km)</th></tr>")

      $.getJSON('all-route-data.json', function(data) {
            $.each(data, function(id, route) {
                  var row = $("<tr />")
                  $("#allRoutesDataTable").append(row); 
                  row.append($("<td>" + id + "</td>"));
                  row.append($("<td>" + "<a href=" + "/routes/" + id + ">" + route.route_name + "</td>"));
                  row.append($("<td>" + route.add_date + "</td>"));
                  row.append($("<td>" + route.route_distance + "</td>"));

              });
      });

});
