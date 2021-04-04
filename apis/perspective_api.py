import os
from dotenv import load_dotenv
from googleapiclient import discovery

# Loading data from .env file
load_dotenv()
api_key = os.getenv('APIKEY')


def perspective_api(chat_data):
    # set thresholds for when to trigger a response
    attributes_thresholds = {
        'INSULT': 0.75,
        'TOXICITY': 0.75,
        'SPAM': 0.75
    }

    # This is the format that API expects
    requested_attributes = {}

    for key in attributes_thresholds:
        requested_attributes[key] = {}

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )

    analyze_request = {
        'comment': {'text': f'{chat_data}'},
        'requestedAttributes': requested_attributes
    }

    response = client.comments().analyze(body=analyze_request).execute()

    data = {}

    for key in response['attributeScores']:
        data[key] = response['attributeScores'][key]['summaryScore']['value'] > attributes_thresholds[key]

    return data
