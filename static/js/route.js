// SAVE A ROUTE ON USER CLICK
function showRouteResults(result){
  alert(result);
}

function saveRoute(evt){
  evt.preventDefault();

  var formInputs = {
    "route": $("#route-name").val(),

    "start_lat": $("#start-lat-field").val(),
    "start_long": $("#start-long-field").val(),
    "end_lat": $("#end-lat-field").val(),
    "end_long": $("#end-long-field").val(),

    "distance":$("#total-distance-field1").val(),
    "favorite":$("#favorite-field1").val()
  }; 
  $.post("/new-route", formInputs, showRouteResults);
}

function validateRouteForm(event){
  event.preventDefault();

  var charInput = $("#route-name").val().length;
  if (charInput < 2) {
    alert("Please enter at least two characters name for the Route");
  } else {
    saveRoute(event);
  }
}

$("#save-route-form").on("submit", validateRouteForm);