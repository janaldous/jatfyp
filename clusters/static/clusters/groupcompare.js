function loadCensusData(variable, question, value) {
  //change text of showing element
  if (question || value) {
    document.getElementById("showing").innerHTML = question + "/" + value;
  } else {
    document.getElementById("showing").innerHTML = "Showing all of group";
  }

}
