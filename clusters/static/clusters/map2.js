// from http://jsfiddle.net/Shreerang/Pp8gT/

function initialize()
{
    var latlng = new google.maps.LatLng(51.458820, -0.117174);
    var latlng2 = new google.maps.LatLng(51.458820, -0.117174);
    var myOptions =
    {
        zoom: 12,
        center: latlng,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };

    var myOptions2 =
    {
        zoom: 12,
        center: latlng2,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };

    var map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);

    var map2 = new google.maps.Map(document.getElementById("map_canvas_2"), myOptions2);

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
    var json2 = JSON.parse(JSON.stringify(json));;

    var mapsArray = [map, map2];

    map.data.addGeoJson(json, { idPropertyName: 'OBJECTID' });
    map2.data.addGeoJson(json2, { idPropertyName: 'OBJECTID' });


    mapsArray.forEach( function(m) {

      m.data.addListener('mouseover', function(event) {
        m.data.revertStyle();
        m.data.overrideStyle(event.feature, {strokeWeight: 8});
      });
      // Set the stroke width, and fill color for each polygon
      m.data.setStyle(styleFeature);
      m.data.addListener('mouseover', mouseInToRegion);
      m.data.addListener('mouseout', mouseOutOfRegion);
    });

    loadCensusData2("/clusters/json/"+cluster_id, null, null, map);
    loadCensusData2("/clusters/json/1", null, null, map2);
    //loadCensusData2("/clusters/json/"+cluster_id, null, null, map);

}

function loadCensusData2(variable, question, value, m) {
  // load the requested variable from the census API (using local copies)
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
        m.data
          .getFeatureById(stateId)
          .setProperty('census_variable', censusVariable);
      } catch(err) {
          console.log("Error = " + variable + "   " + stateId + " " + censusVariable);
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
    document.getElementById("showing").innerHTML = question + "/" + value;
  } else {
    document.getElementById("showing").innerHTML = "Showing all of group";
  }

}
