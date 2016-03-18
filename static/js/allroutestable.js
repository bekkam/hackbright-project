"use strict";

$.getJSON('all-route-data.json', function(data) {
      $.each(data, function(id, route) {
            console.log(id);
            console.log(route);
            var row = $("<tr />")
            $("#allRoutesDataTable").append(row); 
            row.append($("<td>" + id + "</td>"));
            row.append($("<td>" + "<a href=" + "/routes/" + id + ">" + route.route_name + "</td>"));
            row.append($("<td>" + route.add_date + "</td>"));
            row.append($("<td>" + route.route_distance + "</td>"));

        });
});

