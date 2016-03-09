// SAVE A RUN ON USER CLICK
function showRunResults(result){
  alert(result);
}

function saveRun(evt){
  evt.preventDefault();
  alert("save Run fxn called");
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
  alert("end of formInputs");
  $.post("/new-run", formInputs, showRunResults);
}

$("#save-run-form").on("submit", saveRun);