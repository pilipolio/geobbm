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
selected_artist_names = ["Mogwai", "Billy Connolly", "Belle and Sebastian", "Metronomy", "Portishead", "Travis", "Biffy Clyro", "Stereophonics", "Oasis", "Lamb", "The Smiths", "Atomic Kitten"]

selected_artists = [musicbrainz.search_artists(query="country:\"GB\" AND {}".format(name), limit=100)['artist-list'][0] for name in selected_artist_names]
# max limit=100
triphop_artists = musicbrainz.search_artists(query="country:\"GB\" AND tag:trip-hop", limit=100)['artist-list']

artists = selected_artists

geocoded_artists = [
    dict(a.items() + zip(['lat', 'lng'], external_apis.latlng_from_place(a['begin-area']['name'])))
    for a in artists if 'begin-area' in a
    ]

geocoded_artists = [dict(a.items() + [('image', external_apis.get_artist_image_from_bbm(a['name'], size='75'))]) for a in geocoded_artists]
geocoded_artists = [a for a in geocoded_artists if a['image'] !='']


with open("./data/geocoded_artists.json", "w") as f:
    json.dump(geocoded_artists, f)
