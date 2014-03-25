import sys
sys.path.append("../python-musicbrainzngs")

import musicbrainzngs
from musicbrainzngs import musicbrainz
import external_apis

musicbrainzngs.set_useragent("Example music app", "0.1", "http://example.com/music")

# http://musicbrainz.org/ws/2/artist?query=country:%22GB%22%20AND%20tag:trip-hop

# max limit=100
triphop_artists = musicbrainz.search_artists(query="country:\"GB\" AND tag:trip-hop", limit=100)['artist-list']

geocoded_artists = [
    dict(a.items() + zip(['lat', 'lng'], external_apis.latlng_from_place(a['begin-area']['name'])))
    for a in triphop_artists if 'begin-area' in a
    ]

geocoded_artists = [dict(a.items() + [('image', external_apis.get_artist_image_from_bbm(a['name'], size='75'))]) for a in geocoded_artists]
geocoded_artists = [a for a in geocoded_artists if a['image'] !='']

with open("./data/geocoded_artists.json", "w") as f:
    json.dump(geocoded_artists, f)
