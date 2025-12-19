import feedparser
import json
import re
from datetime import datetime

def get_status():
    rss_url = "https://www.reddit.com/r/thedivision/new/.rss"
    feedparser.USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

    try:
        feed = feedparser.parse(rss_url)
        for entry in feed.entries[:20]:
            title = entry.title
            if "the division 2" in title.lower() and "maintenance" in title.lower():
                date_match = re.search(r'([A-Z][a-z]+ \d{1,2}, \d{4})', title)
                if date_match:
                    date_str = date_match.group(1)
                    # Convert "December 19, 2025" into "2025-12-19"
                    try:
                        clean_date = datetime.strptime(date_str, "%B %d, %Y").strftime("%Y-%m-%d")
                        return {
                            "title": title,
                            "url": entry.link,
                            "utc_start": f"{clean_date}T08:30:00Z" # Clean Universal Format
                        }
                    except:
                        continue

        return {"title": "All Systems Nominal", "url": "https://reddit.com/r/thedivision/new/", "utc_start": ""}
    except Exception as e:
        return {"title": "Scanning SHD Network...", "url": "#", "utc_start": ""}

with open('status.json', 'w') as f:
    json.dump(get_status(), f)
