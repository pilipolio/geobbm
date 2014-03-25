import external_apis
# sudo apt-get install python-shapely
import shapely

# https://www.ordnancesurvey.co.uk/opendatadownload/products.html
# http://www.ukpostcode.net/shapefile-of-uk-administrative-counties-wiki-16.html
# ogr2ogr.exe -t_srs WGS84 -f GeoJSON d:\geobbm\data\Map_UK.json d:\geobbm\data\Map_UK.shp



import external_apis
logs = list(external_apis.query_geo_stream_logs('Portishead', size=1000))
logs_points = [geometry.Point(l['geoip.location']) for l in logs]


from shapely import geometry

d = {"type": "Point", "coordinates": (0.0, 0.0)}
geometry.asShape(d)

with open("data/Map_UK_simp_raw.json") as f:
    counties = json.load(f)['features']

counties_polygons = [geometry.asShape(c['geometry']) for c in counties]

# 3358 points for 192 counties
print "%i points for %i counties" % (get_number_of_points(counties_polygons), len(counties_polygons))

def get_number_of_points(geometries):
    return sum(len(g.convex_hull.exterior.coords) for g in geometries if not g.is_empty)

simplified_counties_polygons = [p.simplify(tolerance=0.1, preserve_topology=False) for p in counties_polygons]

# 756 points for 192 counties
print "%i points for %i counties" % (get_number_of_points(simplified_counties_polygons), len(simplified_counties_polygons))


# 500ms per point 
%timeit [[i for i, c in enumerate(counties_polygons) if l.within(c)] for l in logs_points[:1]]

# <1ms per point 
%timeit [[i for i, c in enumerate(simplified_counties_polygons) if l.within(c)] for l in logs_points[:1]]

import itertools
counties_indexes = list(itertools.chain(*[[i for i, c in enumerate(simplified_counties_polygons) if l.within(c)] for l in logs_points]))


# Full workflow
selected_artist_names = ["Mogwai", "Billy Connolly", "Belle and Sebastian", "Metronomy", "Portishead", "Travis", "Biffy Clyro", "Stereophonics", "Oasis", "Lamb", "The Smiths", "Atomic Kitten"]

counties_indexes_per_artists = []
for name in selected_artist_names:
    print name
    logs = list(external_apis.query_geo_stream_logs(name, size=100000))
    logs_points = [geometry.Point(l['geoip.location']) for l in logs]

    print "%i logs fetched from artist" % (len(logs), )

    counties_indexes = list(itertools.chain(*[[i for i, c in enumerate(simplified_counties_polygons) if l.within(c)] for l in logs_points]))
    counties_indexes_per_artists.append(counties_indexes)

with open("data/counties_indexes_per_artists.json", "w") as f:
    json.dump(counties_indexes_per_artists, f)


decorated_counties = [c.copy() for c in counties]
for c in decorated_counties:
    c['properties'] = { 'name': c['properties']['NAME_2']}

for artist_name, counties_indexes in itertools.izip(selected_artist_names, counties_indexes_per_artists):
    for i, count in enumerate(np.bincount(counties_indexes)):
        decorated_counties[i]['properties'][artist_name] = count
    

with open("data/artist_by_counties.json", "w") as f:
    json.dump({'features':decorated_counties, "type": "FeatureCollection"}, f)


# sudo apt-get install libspatialindex-dev
# sudo pip-2.7 install rtree

from rtree import index
counties_index = rtree.index.Index()
count = -1
for i, p in enumerate(counties_polygons):
    counties_index.insert(i, p.bbox)
