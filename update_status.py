import feedparser
import json
import re
from datetime import datetime

def get_status():
    # TRICK: We use the RSS feed and a standard browser identity
    # Many sites allow RSS even when they block scrapers
    rss_url = "https://www.reddit.com/r/thedivision/new/.rss"
    
    # We set a custom User-Agent to avoid the "403 Forbidden" block
    feedparser.USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

    try:
        # Parse the RSS feed with an extra language header some sites require
        feed = feedparser.parse(rss_url, request_headers={'accept-language': 'en-US,en;q=0.9'})
        
        # Check if we got a valid response
        if not feed.entries:
            return {"title": "No Intel Found (Scanning...)", "url": "#", "utc_start": ""}

        maint_post = None
        # Look at the latest 10 posts
        for entry in feed.entries[:10]:
            if "maintenance" in entry.title.lower():
                maint_post = entry
                break
        
        if maint_post:
            title = maint_post.title
            link = maint_post.link
            
            # Extract date from the title (e.g., December 19, 2025)
            date_match = re.search(r'[A-Z][a-z]+ \d{1,2}, \d{4}', title)
            date_str = date_match.group(0) if date_match else "Maintenance Detected"
            
            # Default to standard Ubi time if not found in text
            return {
                "title": title,
                "url": link,
                "utc_start": f"{date_str} 08:30 UTC"
            }

        return {"title": "All Systems Nominal (No Maint Found)", "url": "https://reddit.com/r/thedivision/new", "utc_start": ""}

    except Exception as e:
        return {"title": f"Status Offline: {str(e)}", "url": "#", "utc_start": ""}

# Save the final data
with open('status.json', 'w') as f:
    json.dump(get_status(), f)
