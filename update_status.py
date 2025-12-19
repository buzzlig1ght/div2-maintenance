import requests
import json
from datetime import datetime
import pytz
import re

# 1. Get the latest posts from the subreddit
url = "https://www.reddit.com/r/thedivision/new.json"
headers = {'User-agent': 'Div2StatusBot 0.1'}
response = requests.get(url, headers=headers).json()

# 2. Find the maintenance post
maint_post = None
for post in response['data']['children']:
    title = post['data']['title'].lower()
    if "maintenance" in title:
        maint_post = post['data']
        break

if maint_post:
    title = maint_post['title']
    # Extract the date from the title (e.g., "December 19, 2025")
    # Most Div2 posts follow: "Maintenance - [Date]"
    # We'll just use the post title and current logic for this example
    status_data = {
        "title": title,
        "url": f"https://reddit.com{maint_post['permalink']}",
        "nsw_time": "Check Reddit post for details" # Simple version for now
    }
    
    # Save to a file that the website will read
    with open('status.json', 'w') as f:
        json.dump(status_data, f)
