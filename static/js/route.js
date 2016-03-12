// SAVE A ROUTE ON USER CLICK
function showRouteResults(result){
  alert(result);
}

function saveRoute(evt){
  evt.preventDefault();
  var formValues = $("#save-route-form").serialize();
  $.post("/new-route", formValues, showRouteResults);
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