import json
from shapely import geometry
with open("data/counties_simp250.json") as f:
    counties = json.load(f)['features']
counties_polygons = [geometry.asShape(c['geometry']) for c in counties]

from shapely import ops

uk_multi_polygons = ops.cascaded_union(counties_polygons)