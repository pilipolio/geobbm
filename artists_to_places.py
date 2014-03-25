import sys

sys.path.append("D:\python-musicbrainzngs")

import musicbrainzngs
from musicbrainzngs import musicbrainz

musicbrainzngs.set_useragent("Example music app", "0.1", "http://example.com/music")

artist_id = "f27ec8db-af05-4f36-916e-3d57f91ecf5e"
artist = musicbrainz.get_artist_by_id(artist_id, [])['artist']

print artist

print musicbrainz.get_artist_by_id(artist_id, includes=['area-rels'])


# http://musicbrainz.org/ws/2/artist?query=country:%22GB%22%20AND%20tag:trip-hop

# max limit=100
triphop_artists = musicbrainz.search_artists(query="country:\"GB\" AND tag:trip-hop", limit=100)['artist-list']

geocoded_artists = [
    dict(a.items() + zip(['lat', 'lng'], latlng_from_name_query(a['begin-area']['name'])))
    for a in triphop_artists if 'begin-area' in a
    ]

unique_artist_ids = set(a['id'] for a in triphop_artists)
artist_and_urls = [musicbrainz.get_artist_by_id(artist_id, includes=['url-rels'])['artist'] for artist_id in unique_artist_ids]
# toremove
artist_and_urls = [a['artist'] for a in artist_and_urls]

[get_artist_image(artist) for artist in artist_and_urls]


[get_artist_image(artist) for artist in artist_and_urls]

# artist and urls to image
#artist = musicbrainz.get_artist_by_id('0383dadf-2a4e-4d10-a46a-e9e041da8eb3', includes=['url-rels'])

def get_artist_image(artist):
    if 'url-relation-list' not in artist:
        return ''
    
    possible_image_url = [url for url in artist['url-relation-list'] if url['type'] == 'image']
    return '' if len(possible_image_url) == 0 else possible_image_url[0]['target']

# https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Queen_1984_011.jpg/128px-Queen_1984_011.jpg

unique_area_ids = set(a['artist']['begin-area']['id'] for a['artist'] in artist_and_urls if 'begin-area' in a['artist'])
areas = [musicbrainz.get_area_by_id(area_id, includes=['url-rels']) for area_id in unique_area_ids]
[[url_rel['target'] for url_rel in area['area']['url-relation-list'] if url_rel['type'] == 'geonames'][0] 
    for area in areas]


import urllib2
import json
geoname_id = 3333138

def latlng_from_geonames(geoname_id):
    geonames_query_template = 'http://api.geonames.org/getJSON?formatted=true&geonameId={}&username=pilipolio'
    object = json.load(urllib2.urlopen(url=geonames_query_template.format(geoname_id)))
    return (float(object['lat']), float(object['lng']))

def latlng_from_name_query(name_query):
    geonames_query_template = 'http://api.geonames.org/searchJSON?formatted=true&q={}&maxRows=1&username=pilipolio'
    object = json.load(urllib2.urlopen(url=geonames_query_template.format(urllib2.quote(name_query))))
    place = object["geonames"][0]
    return (float(place['lat']), float(place['lng']))
    
#'http://sws.geonames.org/3333138/about.rdf'
#http://api.geonames.org/getJSON?formatted=true&geonameId=3333138&username=pilipolio
#http://api.geonames.org/getJSON?formatted=true&geonameId=3333138&username=pilipolio&style=full

# area geonames



# http://musicbrainz.org/ws/2/area/34357067-8f7f-4c7a-8d5e-99b6e60f7891?inc=url-rels