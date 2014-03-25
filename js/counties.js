// Draw table from 'jsData' array of objects
function drawTable(tbody, countyProperties) {
    var tr, td;

    for (key in countyProperties) {
        value = countyProperties[key];
        tr = tbody.insertRow(tbody.rows.length);
        td = tr.insertCell(tr.cells.length);
        td.innerHTML = key;
        td = tr.insertCell(tr.cells.length);
        td.innerHTML = value;
        td.setAttribute("align", "center");
        }
}