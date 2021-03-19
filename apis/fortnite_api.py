import json
import requests


def fortnite_api_request(username):
    request_url = f'https://fortnite-api.com/v1/stats/br/v2?name={username}'

    return json.loads(requests.get(
        request_url,
        params={
            'displayName': username
        }
    ).content)
