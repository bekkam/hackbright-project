"use strict";

$.getJSON('tables.json', function(data) {
      $.each(data, function(id, route) {
            console.log(id);
            console.log(route);
            var row = $("<tr />")
            $("#personDataTable").append(row); 
            row.append($("<td>" + id + "</td>"));
            row.append($("<td>" + route.route_name + "</td>"));
            row.append($("<td>" + route.add_date + "</td>"));
            row.append($("<td>" + route.route_distance + "</td>"));

        });
});