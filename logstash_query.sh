curl -XGET 'http://logs.blinkboxmusic.com:9200/logstash-2014.03.25,logstash-2014.03.24/_search?pretty' -d '{
  "query": {
    "filtered": {
      "query": {
        "bool": {
          "must": [
            {
              "query_string": {
                "query": "stream_ARTIST_lookup.raw:\"Birdy\""
              }
            }
          ],
          "should": [
            {
              "query_string": {
                "query": "stream_KEY.raw:\"radiosite\""
              }
            },
            {
              "query_string": {
                "query": "stream_KEY.raw:\"android\""
              }
            },
            {
              "query_string": {
                "query": "stream_KEY.raw:\"iphone\""
              }
            }
          ]
        }
      },
      "filter": {
        "bool": {
          "must": [
            {
              "range": {
                "@timestamp": {
                  "from": 1395671031700,
                  "to": "now"
                }
              }
            },
            {
              "exists": {
                "field": "geoip.location"
              }
            }
          ]
        }
      }
    }
  },
  "fields": [
    "geoip.location",
    "geoip.city_name",
    "stream_ARTIST_lookup"
  ],
  "size": 100,
  "sort": [
    {
      "@timestamp": {
        "order": "desc"
      }
    }
  ]
}'

