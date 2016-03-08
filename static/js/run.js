// SAVE A RUN ON USER CLICK
function showRunResults(result){
  alert(result);
}

function saveRun(evt){
  evt.preventDefault();

  var formInputs = {
    "route": $("#route-name2").val(),

    "start_lat": $("#start-lat-field").val(),
    "start_long": $("#start-long-field").val(),
    "end_lat": $("#end-lat-field").val(),
    "end_long": $("#end-long-field").val(),

    "distance":$("#total-distance-field2").val(),
    "favorite":$("#favorite-field2").val(),
    "date": $("#run-date-field").val(),
    "duration": $("#run-duration-field").val()
  }; 
  $.post("/new-run", formInputs, showRunResults);
}

// function validateRunForm(event){
//   event.preventDefault();

//   // var nameInput = $("#route-name").val().length;
//   var nameInput = $("#route-name").val().length;
//   var dateInput = $("#run-date-field").val().length;
//   var durationInput = $("#run-duration-field").val().length;
 
//   if (nameInput < 2) {
//     alert("Please enter at least two characters name for the Route");
//   } else {
//     saveRun(event);
//   }
// }

$("#save-run-form").on("submit", saveRun);