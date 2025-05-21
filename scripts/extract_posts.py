import json
import requests
import os
from dotenv import load_dotenv
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
SECRET_KEY = os.getenv("SECRET_KEY")
USERNAME = os.getenv("API_USERNAME")
PASSWORD = os.getenv("API_PASSWORD")

api_access_data = {
    'grant_type': 'password',
    'username': USERNAME,
    'password': PASSWORD
}

auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)

headers = {'User-Agent': 'MyAPI/0.0.1'}
res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data= api_access_data, headers=headers)

TOKEN = res.json()['access_token']

headers['Authorization'] = f'bearer {TOKEN}'

#rough = requests.get('https://oauth.reddit.com/api/v1/me', headers=headers).json()
res1 = requests.get('https://oauth.reddit.com/r/developersIndia/hot', headers=headers, params={'limit':'100'})

## EXTRACTION ##
# Fetch and save raw Reddit post data 
posts = res1.json()['data']['children']
raw_posts = [post['data'] for post in posts]  # Extract only the 'data' part

with open("data/rough_redditapi_data.json", "w") as f:
    json.dump(raw_posts, f, indent=2)  # Save as a proper list of post dictionaries

# Load and clean the saved data 
with open("data/rough_redditapi_data.json", "r") as f:
    raw_posts = json.load(f)


## TRANSFORMATION ##
# Imp fields
fields = ["id", "subreddit", "title", "selftext", "ups", "downs",
          "upvote_ratio", "score", "edited", "suggested_sort"]

cleaned_posts = []
for post in raw_posts:
    cleaned_post = {field: post.get(field, None) for field in fields}
    cleaned_posts.append(cleaned_post)

with open("data/cleaned_reddit_data.json", "w") as f:
    for post in cleaned_posts:
        json.dump(post, f)
        f.write("\n")

# Saving only Titles (for comparison)
titles_list = []
for title in res1.json()['data']['children']:
    titles_list.append(title['data']['title'])

with open("data/rough_reddit_titles.json", "w") as f:
    json.dump(titles_list, f, indent=2)