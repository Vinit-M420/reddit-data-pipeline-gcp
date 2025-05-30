from bs4 import BeautifulSoup
import requests,os
from lxml import etree

uri = 'https://www.reddit.com/r/developersIndia/comments/1igteg0/common_traits_of_a_great_developer_you_have/'
request = requests.get(uri)
html_content = request.text
soup = BeautifulSoup(html_content, 'lxml')
post_title = soup.find('h1').text.strip()
with open('data/trait_ofgr8dev.txt', 'w', encoding='utf-8') as f:
    pass  # Just opening in 'w' mode clears the file

with open('data/trait_ofgr8dev.txt', 'a') as f:
    f.write(f"Post title : {post_title} \n\n")


import praw 
import re
from dotenv import load_dotenv

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("SECRET_KEY"),
    username=os.getenv("API_USERNAME"),
    password=os.getenv("API_PASSWORD"),
    user_agent='MyAPI/0.0.1'
)

submission = reddit.submission(url=uri)
submission.comments.replace_more(limit=0)


with open('data/trait_ofgr8dev.txt', 'a', encoding='utf-8') as f:
    for comment in submission.comments[:50]:
        comment_text = comment.body
        
        # Remove blank lines 
        cleaned_text = "\n".join(
            [line.strip() for line in comment_text.splitlines() if line.strip()]
        )
        if re.search(r'https?://\S+', comment_text): ## Skipping comments with contains links
            continue
        
        f.write(f'Comment: {cleaned_text}\n\n')

print('Data saved to txt file')