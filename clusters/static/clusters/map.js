// TODO cite Google maps tutorial
var map;
var censusMin = Number.MAX_VALUE, censusMax = -Number.MAX_VALUE;

function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    zoom: 12,
    center: {lat: 51.458820, lng: -0.117174},
    scrollwheel: false,
    zoomControl: true,
    scaleControl: true,
    draggable: true,
  });

  // wards data from 'https://www.lambeth.gov.uk/sites/default/files/LambethWards_0.json');
  var url = "/static/clusters/data/wards.json";
  var json = (function () {
      var json = null;
      $.ajax({
          'async': false,
          'global': false,
          'url': url,
          'dataType': "json",
          'success': function (data) {
              json = data;
          }
      });
      return json;
  })();
  map.data.addGeoJson(json, { idPropertyName: 'OBJECTID' });

  // When the user hovers, tempt them to click by outlining the letters.
  // Call revertStyle() to remove all overrides. This will use the style rules
  // defined in the function passed to setStyle()
  map.data.addListener('mouseover', function(event) {
    map.data.revertStyle();
    map.data.overrideStyle(event.feature, {strokeWeight: 8});
  });
  loadCensusData("/clusters/json/"+cluster_id);

  // Set the stroke width, and fill color for each polygon
  map.data.setStyle(styleFeature);
  map.data.addListener('mouseover', mouseInToRegion);
  map.data.addListener('mouseout', mouseOutOfRegion);

}

function loadCensusData(variable, question, value) {
  // load the requested variable from the census API (using local copies)
  censusMin = Number.MAX_VALUE;
  censusMax = -Number.MAX_VALUE;
  var xhr = new XMLHttpRequest();
  xhr.open('GET', variable);
  xhr.onload = function() {
    var censusData = JSON.parse(xhr.responseText);
    censusData.shift(); // the first row contains column names
    censusData.forEach(function(row) {
      var censusVariable = parseFloat(row[0]);
      var stateId = row[1];

      // keep track of min and max values
      if (censusVariable < censusMin) {
        censusMin = censusVariable;
      }
      if (censusVariable > censusMax) {
        censusMax = censusVariable;
      }

      // update the existing row with the new data
      try {
        map.data
          .getFeatureById(stateId)
          .setProperty('census_variable', censusVariable);
      } catch(err) {
          console.log("Error = " + variable + "   " + stateId);
      }

      // update and display the legend
      document.getElementById('census-min').textContent =
          censusMin.toLocaleString();
      document.getElementById('census-max').textContent =
          censusMax.toLocaleString();

    });
  };
  xhr.send();

  //change text of showing element
  if (question || value) {
    document.getElementById("showing-question").innerHTML = truncate(question);
    document.getElementById("showing-choice").innerHTML = truncate(value);
    document.getElementById("showing-cluster").innerHTML = variable.split("/")[4];
  } else {
    document.getElementById("showing-question").innerHTML = "Showing all of group";
    document.getElementById("showing-choice").innerHTML = "";
    document.getElementById("showing-cluster").innerHTML = "";
  }

}

function styleFeature(feature) {
  var low = [5, 69, 54];  // color of smallest datum
  var high = [151, 83, 34];   // color of largest datum

  // delta represents where the value sits between the min and max
  var delta = (feature.getProperty('census_variable') - censusMin) /
      (censusMax - censusMin);

  var color = [];
  for (var i = 0; i < 3; i++) {
    // calculate an integer color based on the delta
    color[i] = (high[i] - low[i]) * delta + low[i];
  }

  // determine whether to show this shape or not
  var showRow = true;
  if (feature.getProperty('census_variable') == null ||
      isNaN(feature.getProperty('census_variable'))) {
    showRow = false;
  }

  var outlineWeight = 0.5, zIndex = 1;
  if (feature.getProperty('state') === 'hover') {
    outlineWeight = zIndex = 2;
  }

  return {
    strokeWeight: outlineWeight,
    strokeColor: '#fff',
    zIndex: zIndex,
    fillColor: 'hsl(' + color[0] + ',' + color[1] + '%,' + color[2] + '%)',
    fillOpacity: 0.75,
    visible: showRow
  };
}

/**
 * Responds to the mouse-in event on a map shape (state).
 *
 * @param {?google.maps.MouseEvent} e
 */
function mouseInToRegion(e) {
  // set the hover state so the setStyle function can change the border
  e.feature.setProperty('state', 'hover');

  var percent = (e.feature.getProperty('census_variable') - censusMin) /
      (censusMax - censusMin) * 100;

  // update the label
  document.getElementById('data-label').textContent =
      e.feature.getProperty('NAME');
  document.getElementById('data-value').textContent =
      e.feature.getProperty('census_variable').toLocaleString();
  document.getElementById('data-box').style.display = 'block';
  document.getElementById('data-caret').style.display = 'block';
  document.getElementById('data-caret').style.paddingLeft = percent + '%';
}

/**
 * Responds to the mouse-out event on a map shape (state).
 *
 * @param {?google.maps.MouseEvent} e
 */
function mouseOutOfRegion(e) {
  // reset the hover state, returning the border to normal
  e.feature.setProperty('state', 'normal');
}

/** adapted from http://stackoverflow.com/questions/4700226/i-want-to-truncate-a-text-or-line-with-ellipsis-using-javascript **/
function truncate(string){
  var len = 50;
   if (string.length > len)
      return string.substring(0,len)+'...';
   else
      return string;
};
