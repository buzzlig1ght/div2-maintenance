import requests
import json
import re

# We use a very standard browser identity
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json',
    'Referer': 'https://old.reddit.com/r/thedivision/'
}

def get_status():
    try:
        # TRICK: We use old.reddit.com which is often less restrictive
        url = "https://old.reddit.com/r/thedivision/new.json?limit=10"
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code != 200:
            return {"title": f"Reddit Blocked Us (Error {response.status_code})", "url": "#", "utc_start": ""}

        data = response.json()
        maint_post = None
        
        for post in data['data']['children']:
            title = post['data'].get('title', '').lower()
            # We look for "maintenance" and today's date format (e.g. "December")
            if "maintenance" in title:
                maint_post = post['data']
                break

        if maint_post:
            full_title = maint_post['title']
            text = maint_post.get('selftext', '')
            
            # Detect Summer/Winter time
            utc_start_hour = "07:30" if "CEST" in text else "08:30"
            
            # Find date in title (e.g. December 19, 2025)
            date_match = re.search(r'[A-Z][a-z]+ \d{1,2}, \d{4}', full_title)
            date_str = date_match.group(0) if date_match else "Upcoming"

            return {
                "title": full_title,
                "url": f"https://reddit.com{maint_post['permalink']}",
                "utc_start": f"{date_str} {utc_start_hour} UTC"
            }
        
        return {"title": "No current maintenance found", "url": "#", "utc_start": ""}

    except Exception as e:
        return {"title": f"Script Error: {str(e)}", "url": "#", "utc_start": ""}

# Save and overwrite the status.json
with open('status.json', 'w') as f:
    json.dump(get_status(), f)
