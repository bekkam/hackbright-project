"use strict";

// Save a run on user click
function showRunResults(result){
  alert(result);
}

function saveRun(evt){
  evt.preventDefault();
  var saveRunFormValues = $("#save-run-form").serialize();
  $.post("/new-run", saveRunFormValues, showRunResults);
}

function validateRunForm(event){
  event.preventDefault();

  var charInput = $("#route-name2").val().length;
  var duration = $("#run-duration-field").val();
  if (charInput < 2) {
    alert("Please enter at least two characters name for the Route");
    // Alert the user if their input for duration is not purely numeric
  } else if (isNaN(+duration) == true) {
    alert("Please enter a number for the duration of the Route");
  } else {
    saveRun(event);
  }
}

$("#save-run-form").on("submit", validateRunForm);