"use strict";


// ################ Utility Methods for Form Validation #########################
function checkMinimumInputLength(inputLength) {
    return inputLength < 2 ? false : true;
}

function checkDateFormat(date) {
// return false if date is not in mm/dd/yyy format

    var re = /^\d{2}?\/\d{2}?\/\d{4}?$/;
    if (date.search(re) == -1) {
        return false;
    }
}

function checkDateBoundaries(date) {
// return false if date does not exist, or is out of bounds

    var date_elements = date.split("/");
    var day = parseInt(date_elements[1], 10);
    var month = parseInt(date_elements[0], 10);
    var year = parseInt(date_elements[2], 10);

    // Check the ranges of month and year
    if (year < 1990 || year > 2016 || month == 0 || month > 12) {
        return false;
    }

    var monthLength = [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ];

    // Adjust for leap years
    if (year % 400 == 0 || (year % 100 != 0 && year % 4 == 0)) {
        monthLength[1] = 29;
    }
    // Check the range of the day
    return day > 0 && day <= monthLength[month - 1];
}

function checkDurationType(duration) {
// return false if duration is not purely numeric
    var re = /^\d*$/;

    if (duration.search(re) == -1) {
        return false;
    }
}


// ############### Utility Methods for Submitting Forms ###########

function showResults(result) {
// show user a confirmatory message
    alert(result);
}

function saveToDb(evt, url) {
// send form data to server

    evt.preventDefault();

    // get the id for the form
    var id = evt.currentTarget.id;
    var formValues = $("#" + id +"").serialize();

    $.post(url, formValues, showResults);
}


// ############### Methods to Validate Forms ###########

function validateRunForm(event) {

    event.preventDefault();

    var charInput = $("#route-name2").val().length;
    var runDate = $("#run-date-field").val();
    var duration = $("#run-duration-field").val();

    // validate form fields. only submit to server if all fields are valid.
    if (checkMinimumInputLength(charInput) == false) {
        alert("Please enter at least two characters for the name of the Route");

    } else if (checkDateFormat(runDate) == false) {
        alert("Please enter a run date in appropriate format");

    } else if (checkDateBoundaries(runDate) == false) {
        alert("That date is out of range. " +
              "Please enter a date from 01/01/1990 to present");

    } else if (checkDurationType(duration) == false) {
        alert("Please enter a number for the duration of the Run");

    } else {
        saveToDb(event, "/new-run");
    }
}

$("#save-run-form").on("submit", validateRunForm);


function validateRouteForm(event){
    event.preventDefault();

    var charInput = $("#route-name").val().length;

    if (checkMinimumInputLength(charInput) == false) {
        alert("Please enter at least two characters for the name of the Route");

    } else {
        saveToDb(event, "/new-course");
    }
}

$("#save-course-form").on("submit", validateRouteForm);


// ####################  Datepicker ##############################

$(document).ready(function() {
    $( "#run-date-field" ).datepicker({ maxDate: "+0D" });
});

