import feedparser
import json
import re
from datetime import datetime

def get_status():
    # Official Ubisoft News Feed for Division 2
    feed_url = "https://www.ubisoft.com/en-us/game/the-division/the-division-2/news-updates/rss"
    feed = feedparser.parse(feed_url)
    
    maint_item = None
    # Look through the last 5 news items
    for entry in feed.entries[:5]:
        if "maintenance" in entry.title.lower():
            maint_item = entry
            break
            
    if maint_item:
        # Most Ubi news items have the date in the title or link
        title = maint_item.title
        url = maint_item.link
        
        # We'll use the "Published" date from the feed as the maintenance date
        # and assume the standard 08:30 UTC start time
        date_obj = datetime(*maint_item.published_parsed[:6])
        date_str = date_obj.strftime("%B %d, %Y")

        return {
            "title": title,
            "url": url,
            "utc_start": f"{date_str} 08:30 UTC"
        }
    
    return {"title": "No Maintenance Found in News Feed", "url": "https://www.ubisoft.com/en-us/game/the-division/the-division-2/news-updates", "utc_start": ""}

# Save the data
with open('status.json', 'w') as f:
    json.dump(get_status(), f)
