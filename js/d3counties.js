oldDrawAccordingToProjection = function(svg, className, projection, featureCollection)
{
    // http://stackoverflow.com/questions/14492284/center-a-map-in-d3-given-a-geojson-object
    // Create a unit projection.
    var projection = projection
        .scale(1)
        .translate([0, 0]);

    var path = d3.geo.path().projection(projection);

    // Compute the bounds of a feature of interest, then derive scale & translate.
    var b = path.bounds(featureCollection),
    s = 1.0 / Math.max((b[1][0] - b[0][0]) / width, (b[1][1] - b[0][1]) / height),
    t = [(width - s * (b[1][0] + b[0][0])) / 2, (height - s * (b[1][1] + b[0][1])) / 2];

    projection.scale(s).translate(t);

    var path = d3.geo.path().projection(projection);

    return svg.selectAll(className)
      .data(featureCollection.features)
      .enter().append("path")
      .attr("d", path);
}

drawAccordingToProjection = function(projection, featureCollection, featurePaths)
{
    // http://stackoverflow.com/questions/14492284/center-a-map-in-d3-given-a-geojson-object
    // Create a unit projection.
    var projection = projection
        .scale(1)
        .translate([0, 0]);

    var path = d3.geo.path().projection(projection);

    // Compute the bounds of a feature of interest, then derive scale & translate.
    var b = path.bounds(featureCollection),
    s = 1.0 / Math.max((b[1][0] - b[0][0]) / width, (b[1][1] - b[0][1]) / height),
    t = [(width - s * (b[1][0] + b[0][0])) / 2, (height - s * (b[1][1] + b[0][1])) / 2];

    projection.scale(s).translate(t);

    var path = d3.geo.path().projection(projection);

    return featurePaths.attr("d", path);
}
