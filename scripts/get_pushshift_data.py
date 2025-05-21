import os
import json
import requests

url = 'https://api.pushshift.io/reddit/search/submission/?subreddit=developersIndia&size=10'

response = requests.get(url,timeout=10)

api_data = response.json()

with open('data/rough_pushshift_data.json', 'w') as f:
    json.dump(api_data, f, indent=4)

## Pushshift API has cracked down on free access for Developers