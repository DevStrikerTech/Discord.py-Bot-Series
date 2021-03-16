import os
import json
import requests
from dotenv import load_dotenv

# Loading data from .env file
load_dotenv()
client_id = os.getenv('CLIENTID')
client_secret = os.getenv('CLIENTSECRET')


def compiler(code):
    post_url = 'https://api.jdoodle.com/v1/execute'

    return json.loads(requests.post(
        post_url,
        json={
            "script": f"{code}",
            "language": "python3",
            "versionIndex": "3",
            "clientId": f"{client_id}",
            "clientSecret": f"{client_secret}"
        }
    ).content)
