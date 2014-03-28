import external_apis
# sudo apt-get install python-shapely
import shapely

# https://www.ordnancesurvey.co.uk/opendatadownload/products.html
# http://www.ukpostcode.net/shapefile-of-uk-administrative-counties-wiki-16.html
# ogr2ogr.exe -t_srs WGS84 -f GeoJSON d:\geobbm\data\Map_UK.json d:\geobbm\data\Map_UK.shp



import external_apis
from shapely import geometry

with open("data/Map_UK_simp_raw.json") as f:
    counties = json.load(f)['features']

counties_polygons = [geometry.asShape(c['geometry']) for c in counties]

# 3358 points for 192 counties
print "%i points for %i counties" % (get_number_of_points(counties_polygons), len(counties_polygons))

def get_number_of_points(geometries):
    return sum(len(g.convex_hull.exterior.coords) for g in geometries if not g.is_empty)

simplified_counties_polygons = [p.simplify(tolerance=0.05, preserve_topology=False) for p in counties_polygons]

# 756 points for 192 counties
print "%i points for %i counties" % (get_number_of_points(simplified_counties_polygons), len(simplified_counties_polygons))


# 500ms per point 
%timeit [[i for i, c in enumerate(counties_polygons) if l.within(c)] for l in logs_points[:1]]

# <1ms per point 
%timeit [[i for i, c in enumerate(simplified_counties_polygons) if l.within(c)] for l in logs_points[:1]]

import itertools
counties_indexes = list(itertools.chain(*[[i for i, c in enumerate(simplified_counties_polygons) if l.within(c)] for l in logs_points]))


# Full workflow
selected_artist_queries = [
    {"artist":"Metronomy", "ndays":5}, {"artist":"Travis", "ndays":3}, {"artist":"Biffy Clyro", "ndays":2}, {"artist":"Stereophonics", "ndays":2}, {"artist":"Oasis", "ndays":2, "tag":"britpop"}, {"artist":"The Smiths", "ndays":3}, {"artist":"Atomic Kitten", "ndays":5}, {"artist":"Tom Jones", "ndays":5}, {"artist":"Dizzee Rascal", "ndays":2}, {"artist":"Ed Sheeran", "ndays":1}, {"artist":"Radiohead", "ndays":3}, {"artist":"The Animals", "ndays":10}]


raw_logs_per_artists = []
for query in selected_artist_queries:
    print query
    logs = list(external_apis.query_geo_stream_logs(query['artist'], size=100000, ndays=query['ndays']))
    raw_logs_per_artists.append(logs)
    print "%i logs fetched from artist" % (len(logs), )


import pickle
with open("data/raw_logs_per_artists.pck", "w") as f:
    pickle.dump(raw_logs_per_artists, f)

counties_indexes_per_artists = []

for query, logs in zip(selected_artist_queries, raw_logs_per_artists):
    print query
    logs_points = [geometry.Point(l['geoip.location']) for l in logs]
    counties_indexes = list(itertools.chain(*[[i for i, c in enumerate(simplified_counties_polygons) if l.within(c)] for l in logs_points]))
    counties_indexes_per_artists.append(counties_indexes)


import numpy as np
artist_county_counts = np.array([np.bincount(indexes) for indexes in counties_indexes_per_artists])

artist_national_percents = 100 * artist_county_counts.sum(axis=1, dtype=np.float) / artist_county_counts.sum()
county_grand_total = artist_county_counts.sum(axis=0, dtype=np.float)
artist_county_local_percents = 100 * (artist_county_counts / county_grand_total)

artist_county_deviations_percents = (artist_county_local_percents.T - artist_national_percents).T

decorated_counties = [c.copy() for c in counties]
for c in decorated_counties:
    c['properties'] = { 'name': c['properties']['NAME_2']}

for artist_name, counties_values in itertools.izip(selected_artist_names, artist_county_deviations_percents.tolist()):
    for i, value in enumerate(counties_values):
        decorated_counties[i]['properties'][artist_name] = value
    

with open("data/artist_by_counties.json", "w") as f:
    json.dump({'features':decorated_counties, "type": "FeatureCollection"}, f)


# sudo apt-get install libspatialindex-dev
# sudo pip-2.7 install rtree

from rtree import index
counties_index = rtree.index.Index()
count = -1
for i, p in enumerate(counties_polygons):
    counties_index.insert(i, p.bbox)
