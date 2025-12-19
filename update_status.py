import requests
import json
import re
import sys

# 1. We use a more specific "User-Agent" so Reddit doesn't block us
headers = {
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Div2MaintBot/1.0 (by /u/YOUR_REDDIT_USERNAME_HERE)'
}

def get_status():
    try:
        url = "https://www.reddit.com/r/thedivision/new.json"
        response = requests.get(url, headers=headers)
        
        # Check if Reddit actually gave us data
        if response.status_code != 200:
            return {"title": f"Reddit error: {response.status_code}", "url": "#", "utc_start": ""}

        data = response.json()
        maint_post = None
        
        for post in data['data']['children']:
            title = post['data'].get('title', '').lower()
            if "maintenance" in title:
                maint_post = post['data']
                break

        if maint_post:
            full_title = maint_post['title']
            text = maint_post.get('selftext', '')
            
            # Detect Summer Time (CEST) or Winter Time (CET)
            utc_start_hour = "07:30" if "CEST" in text else "08:30"
            
            # Find date like "December 19, 2025"
            date_match = re.search(r'[A-Z][a-z]+ \d{1,2}, \d{4}', full_title)
            date_str = date_match.group(0) if date_match else "Upcoming"

            return {
                "title": full_title,
                "url": f"https://reddit.com{maint_post['permalink']}",
                "utc_start": f"{date_str} {utc_start_hour} UTC"
            }
        
        return {"title": "No recent maintenance found", "url": "#", "utc_start": ""}

    except Exception as e:
        return {"title": f"Script Error: {str(e)}", "url": "#", "utc_start": ""}

# Save the result
final_data = get_status()
with open('status.json', 'w') as f:
    json.dump(final_data, f)

print(f"Successfully updated: {final_data['title']}")
