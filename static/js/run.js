"use strict";

// Save a run on user click
function showRunResults(result) {

    alert(result);
}

function saveRun(evt) {

    evt.preventDefault();
    // console.log("called saveRun function");
    var saveRunFormValues = $("#save-run-form").serialize();

    $.post("/new-run", saveRunFormValues, showRunResults);
}

function validateRunForm(event) {

    event.preventDefault();

    var charInput = $("#route-name2").val().length;
    var runDate = $("#run-date-field").val();
    var duration = $("#run-duration-field").val();

    // Alert user is they are missing a date
    if (charInput < 2) {
        alert("Please enter at least two characters name for the Route");

      // Alert user is they are missing a date
    } else if (isNaN(runDate) == false) {
        alert("Please enter a run date");

      // Alert the user if their input for duration is not purely numeric, or is absent
    } else if (isNaN(duration) == false) {
        alert("Please enter a value for the duration of the Run");

    } else if (typeof(duration) != 'number') {
        alert("Please enter a number for the duration of the Run");

    } else {
        saveRun(event);
    }
}

$("#save-run-form").on("submit", validateRunForm);


$(document).ready(function() {
    $( "#run-date-field" ).datepicker({ maxDate: "+0D" });
});

