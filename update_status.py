import feedparser
import json
import re

def get_status():
    rss_url = "https://www.reddit.com/r/thedivision/new/.rss"
    # Identity fix to stop the 403 blocks
    feedparser.USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

    try:
        feed = feedparser.parse(rss_url)
        
        # We search specifically for the official announcement title format
        # Example: "The Division 2 - Maintenance - December 19, 2025"
        for entry in feed.entries[:20]:
            title = entry.title
            # STRICK CHECK: Must contain "The Division 2", "Maintenance", and a date
            if "the division 2" in title.lower() and "maintenance" in title.lower():
                # Extract the specific date from the title
                date_match = re.search(r'[A-Z][a-z]+ \d{1,2}, \d{4}', title)
                if date_match:
                    date_str = date_match.group(0)
                    return {
                        "title": title,
                        "url": entry.link,
                        "utc_start": f"{date_str} 08:30 UTC"
                    }

        # If we can't find a "New" post, it means there is no maintenance today.
        return {
            "title": "All Systems Nominal",
            "url": "https://www.reddit.com/r/thedivision/new/",
            "utc_start": ""
        }

    except Exception as e:
        return {"title": "Scanning SHD Network...", "url": "#", "utc_start": ""}

with open('status.json', 'w') as f:
    json.dump(get_status(), f)
