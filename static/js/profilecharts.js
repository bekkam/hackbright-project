
// Line chart for user's run distance over time
var options = {
  responsive: false,
  scaleBeginAtZero: false
};
var ctxLineDistance = $("#lineChartDistance").get(0).getContext("2d");

$.get("/user-distance.json", function (data) {
  var lineChartUserDistance = new Chart(ctxLineDistance).Line(data, options);
  $("#lineLegendDistance").html(lineChartUserDistance.generateLegend());
});

// Line chart for user's running pace over time
var options = {
  responsive: false,
  scaleBeginAtZero: false
};
var ctxLinePace = $("#lineChartPace").get(0).getContext("2d");

$.get("/user-pace.json", function (data) {
  var lineChartUserPace = new Chart(ctxLinePace).Line(data, options);
  $("#lineLegendPace").html(lineChartUserPace.generateLegend());
});