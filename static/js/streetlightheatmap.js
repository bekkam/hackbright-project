var latLngs = [];

function generateHeatMap(evt) {
  alert("generateHeatMap called");
  // Make the query string for SODA API
  url = "https://data.sfgov.org/resource/vw6y-z8j6.json?"
    +"category=Streetlights"
    +"&Status=Open"

    // Get data, and lat/long to latLngs array
    $.getJSON(url, function(data) {
      console.log(data);
          $.each(data, function(i, entry) {
              latLngs.push(new google.maps.LatLng(parseFloat(entry.point.latitude), 
                                                   parseFloat(entry.point.longitude)));
            });
    });
    var heatmap = new google.maps.visualization.HeatmapLayer({
        data: latLngs,
        map: map
    }); 
}

$("#heatmap").on("change", generateHeatMap);
