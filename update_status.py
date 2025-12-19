import feedparser
import json
import re
from datetime import datetime, timedelta

def get_status():
    rss_url = "https://www.reddit.com/r/thedivision/new/.rss"
    feedparser.USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

    try:
        feed = feedparser.parse(rss_url)
        for entry in feed.entries[:20]:
            title = entry.title
            # We check the title for "Maintenance" and a date
            if "the division 2" in title.lower() and "maintenance" in title.lower():
                date_match = re.search(r'([A-Z][a-z]+ \d{1,2}, \d{4})', title)
                if date_match:
                    date_str = date_match.group(1)
                    # Standard start is 08:30 UTC
                    start_time = datetime.strptime(date_str, "%B %d, %Y").replace(hour=8, minute=30)
                    
                    # Search body for "X hours", default to 5 if not found
                    content = entry.summary.lower()
                    duration_match = re.search(r'(\d+)\s*hour', content)
                    duration = int(duration_match.group(1)) if duration_match else 5
                    
                    end_time = start_time + timedelta(hours=duration)

                    return {
                        "title": title,
                        "url": entry.link,
                        "utc_start": start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                        "utc_end": end_time.strftime("%Y-%m-%dT%H:%M:%SZ")
                    }

        return {"title": "All Systems Nominal", "url": "https://reddit.com/r/thedivision/new/", "utc_start": "", "utc_end": ""}
    except Exception as e:
        return {"title": "SHD Link Offline", "url": "#", "utc_start": "", "utc_end": ""}

with open('status.json', 'w') as f:
    json.dump(get_status(), f)
