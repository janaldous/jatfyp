function changeText(variable, question, value) {
  //change text of showing element
  if (question || value) {
    document.getElementById("showing-question").innerHTML = truncate(question);
    document.getElementById("showing-choice").innerHTML = truncate(value);
    try { document.getElementById("showing-cluster").innerHTML = variable.split("/")[4]; } catch(err) {}
  } else {
    document.getElementById("showing-question").innerHTML = "Showing all of group";
    document.getElementById("showing-choice").innerHTML = "";
    try { document.getElementById("showing-cluster").innerHTML = ""; } catch(err) {}
  }

}

function truncate(string){
  var len = 50;
   if (string.length > len)
      return string.substring(0,len)+'...';
   else
      return string;
};
