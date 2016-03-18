"use strict";


// function drawTable(data) {
//     alert("drawTable called");
//     console.log(data);
//     console.log(data.keys.length);
//     for (var i = 0; i < data.length; i++) {
//         drawRow(data[i]);
//     }
// }

// function drawRow(rowData) {
//     alert("drawRow called");
//     console.log(rowData);
//     var row = $("<tr />")
//     $("#personDataTable").append(row); //this will append tr element to table... keep its reference for a while since we will add cels into it
//     row.append($("<td>" + rowData.route_name + "</td>"));
//     row.append($("<td>" + rowData.route_id + "</td>"));
// }


// $.get('/tables.json', drawRow);
//  {
//     alert("anon function called");
// };



$.getJSON('tables.json', function(data) {
      $.each(data, function(id, route) {
            console.log(id);
            console.log(route);
            var row = $("<tr />")
            $("#personDataTable").append(row); 
            row.append($("<td>" + id + "</td>"));
            row.append($("<td>" + route.route_name + "</td>"));
            // row.append($("<td>" + route.add_date + "</td>"));
            row.append($("<td>" + route.route_distance + "</td>"));

        });
});