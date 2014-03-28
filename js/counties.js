// Draw table from 'jsData' array of objects
function drawTable(tbody, countyProperties) {
    var tr, td;

    for (key in countyProperties) {
        if (key == 'name')
        {
            continue
        }
        value = countyProperties[key];
        tr = tbody.insertRow(tbody.rows.length);
        td = tr.insertCell(tr.cells.length);
        td.innerHTML = key;
        td = tr.insertCell(tr.cells.length);
        td.innerHTML = value.toFixed(1);
        td.setAttribute("align", "center");
    }
}

function getColor(d) {
    return d > 25 ? '#800026' :
           d > 10  ? '#BD0026' :
           d > 5  ? '#E31A1C' :
           d > 1  ? '#FC4E2A' :
           d < 1   ? '#FD8D3C' :
           d < 5   ? '#FEB24C' :
           d < 10   ? '#FED976' :
                      '#FFEDA0';
}


// global styler for geojson areas
var areaStyler = {
    // The feature property's key whom value will be use for coloring. 
    propertyKey: "NOT_SET",
    getAreaStyle: function(feature) {
        console.log("set feature's style with key = " + this.propertyKey)
        return {
            fillColor: this.propertyKey in feature.properties ? getColor(feature.properties[this.propertyKey]) : 'grey',
            weight: 2,
            opacity: 1,
            color: 'black',
            dashArray: '3',
            fillOpacity: 0.7
        };
    }
};


function highlightFeature(e) {
    var layer = e.target;

    layer.setStyle({
        weight: 5,
        //color: '#666',
        dashArray: '',
        fillOpacity: 0.7
    });

    if (!L.Browser.ie && !L.Browser.opera) {
        layer.bringToFront();
    }
}

