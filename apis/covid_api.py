import json
import urllib.request


def covid_api_request(endpoint):
    covid_request_url = urllib.request.Request('https://api.covid19api.com/' + endpoint)
    covid_request_data = json.loads(urllib.request.urlopen(covid_request_url).read().decode('utf-8'))

    return covid_request_data
