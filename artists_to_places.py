import sys
sys.path.append("../python-musicbrainzngs")
import json

import musicbrainzngs
from musicbrainzngs import musicbrainz
import external_apis

musicbrainzngs.set_useragent("Example music app", "0.1", "http://example.com/music")

# http://musicbrainz.org/ws/2/artist?query=country:%22GB%22%20AND%20tag:trip-hop

# selected artists
#http://musicbrainz.org/tag/scottish/artist
#http://musicbrainz.org/tag/welsh/artist?page=2
# http://www.blinkboxmusic.com/listen/i/s2054/Welsh-Pop/radio
selected_artist_queries = [
    {"artist":"Metronomy", "ndays":7}, {"artist":"Travis", "ndays":4}, {"artist":"Biffy Clyro", "ndays":4}, {"artist":"Stereophonics", "ndays":2}, {"artist":"Oasis", "ndays":2, "tag":"britpop"}, {"artist":"The Smiths", "ndays":4}, {"artist":"Atomic Kitten", "ndays":3}, {"artist":"Tom Jones", "ndays":7}, {"artist":"Dizzee Rascal", "ndays":2}, {"artist":"Ed Sheeran", "ndays":2}, {"artist":"Radiohead", "ndays":4}, {"artist":"The Animals", "ndays":7}]

selected_artist_names = [query['artist'] for query in selected_artist_queries]

def musicbrainz_query(**kwargs):
    if "tag" in kwargs:
        return "country:\"GB\" AND artist:{artist} AND tag:{tag}".format(**kwargs)
    else:
        return "country:\"GB\" AND artist:{artist}".format(**kwargs)
    

selected_artists = [musicbrainz.search_artists(query=musicbrainz_query(**query), limit=1)['artist-list'][0] for query in selected_artist_queries]

# max limit=100
triphop_artists = musicbrainz.search_artists(query="country:\"GB\" AND tag:trip-hop", limit=100)['artist-list']

artists = selected_artists

geocoded_artists = [
    dict(a.items() + zip(['lat', 'lng'], external_apis.latlng_from_place(a['begin-area']['name'] +  ", United Kingdom")))
    for a in artists if 'begin-area' in a
    ]

geocoded_artists = [dict(a.items() + [('image', external_apis.get_artist_image_from_bbm(a['name'], size='75'))]) for a in geocoded_artists]
geocoded_artists = [a for a in geocoded_artists if a['image'] !='']


with open("./data/geocoded_artists.json", "w") as f:
    f.write("var artists = " + json.dumps(geocoded_artists)) 
    
