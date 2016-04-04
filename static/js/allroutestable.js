"use strict";

$( document ).ready(function() {
      $('#allCoursesDataTable').html("<tr><th>Course ID</th><th>Course Name</th><th>Date Added</th><th>Distance (km)</th></tr>")

      $.getJSON('all-course-data.json', function(data) {
            $.each(data, function(id, course) {
                  var row = $("<tr />")
                  $("#allCoursesDataTable").append(row); 
                  row.append($("<td>" + id + "</td>"));
                  row.append($("<td>" + "<a href=" + "/courses/" + id + ">" + course.route_name + "</td>"));
                  row.append($("<td>" + course.add_date + "</td>"));
                  row.append($("<td>" + course.route_distance + "</td>"));

              });
      });

});
