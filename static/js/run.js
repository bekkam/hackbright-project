// SAVE A RUN ON USER CLICK
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

  var charInput = $("#run-name").val().length;
  if (charInput < 2) {
    alert("Please enter at least two characters name for the Route");
  } else {
    saveRoute(event);
  }
}


$("#save-run-form").on("submit", saveRun);