
  "use strict";
  // var map;

  function initMap() {
     alert("called initMap");

     var map = new google.maps.Map(document.getElementById('map'), {
      zoom: 14,
      center: {lat: 37.7833, lng: -122.4167 }
    });
  }



