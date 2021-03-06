import urllib2
import json

GEONAMES_USER_NAME = "pilipolio"

def latlng_from_geonames(geoname_id):
    """
    Return a (lat, lng) from a geoname_id using http://api.geonames.org.
    >>> latlng_from_geonames(3333138)
    (51.54281, -0.15942)
    """
    geonames_query_template = 'http://api.geonames.org/getJSON?formatted=true&geonameId={geoname_id}&username={user_name}'
    place_lookup_result = json.load(urllib2.urlopen(url=geonames_query_template.format(geoname_id=geoname_id, user_name=GEONAMES_USER_NAME)))
    return (float(place_lookup_result['lat']), float(place_lookup_result['lng']))

def latlng_from_place(name):
    """
    Return a (lat, lng) from a place name using http://api.geonames.org.
    >>> latlng_from_place("Oxford, United Kingdom")
    (51.75222, -1.25596)
    """
    geonames_query_template = 'http://api.geonames.org/searchJSON?formatted=true&q={query}&maxRows=1&username={user_name}'
    search_results = json.load(urllib2.urlopen(url=geonames_query_template.format(query=urllib2.quote(name), user_name=GEONAMES_USER_NAME)))
    place = search_results["geonames"][0]
    return (float(place['lat']), float(place['lng']))
    
BBM_SEARCH_URL = "https://api.stagingc.we7.com/api/0.1/simpleSearch"

def get_artist_image_from_bbm(artist_name, size="original"):
    """
    Use bbm simple search api to return an artist image url.
    >>> get_artist_image_from_bbm("portishead")
    u'http://images.stagingc.blinkboxmusic.com/image/original/121624.jpg'
    """
    simple_search_template = "{search_url}?apiKey=test&appVersion=1&format=json&type=artists&query={query}&limit=1&imageSizes={sizes}"
    search_results = json.load(urllib2.urlopen(url=simple_search_template.format(search_url=BBM_SEARCH_URL, query=urllib2.quote(artist_name), sizes=size)))
    return search_results['artists'][0]['images'][size] if len(search_results['artists']) == 1 else ''

import urllib2
import datetime

def query_geo_stream_logs(artist_name, size=1000, ndays=1):
    """ Query logstash for a given artist
    """
    past_days = [datetime.datetime.now() - datetime.timedelta(days=i) for i in range(ndays)]
    logstash_url = 'https://logs.blinkboxmusic.com/{csv_days}/_search?pretty'.format(
        csv_days=",".join("logstash-{:%Y.%m.%d}".format(d) for d in past_days))

    with open("logstash_query.json") as f:
        logstash_query = json.load(f)

    # currently does not use range
    #now = datetime.datetime.utcnow()
    #(now - datetime.datetime(1970, 1, 1)).total_seconds()
    logstash_query['query']['filtered']['filter']['bool']['must'] = [{"exists": { "field": "geoip.location"}}]
    # Replace artist filter in the template
    logstash_query['query']['filtered']['query']['bool']['must'][0]['query_string']['query'] = u'stream_ARTIST_lookup.raw:"{artist_name}"'.format(artist_name=artist_name)
    logstash_query['size'] = size
    u = urllib2.urlopen(logstash_url, data=json.dumps(logstash_query), timeout=60 * 60)

    logs = json.load(u.fp)
    return (l['fields'] for l in logs['hits']['hits'])
