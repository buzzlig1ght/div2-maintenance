import requests
import json
import re

def get_status():
    # This URL specifically targets the Ubisoft Help "Live Feed" for Div 2
    url = "https://ubistatic-a.akamaihd.net/0115/tctd2/status.html"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            # We look for the "Maintenance" section in their status page
            if "Maintenance" in response.text:
                return {
                    "title": "Maintenance Detected",
                    "url": "https://www.ubisoft.com/en-us/help/game/the-division-2",
                    "utc_start": "Check Ubisoft Help for exact time"
                }
        
        # If the official status page is blank (classic Ubisoft), 
        # let's use a "Safety" message
        return {
            "title": "No major maintenance reported by Ubisoft",
            "url": "https://www.reddit.com/r/thedivision/new/",
            "utc_start": ""
        }
    except:
        return {"title": "Status Feed Offline", "url": "#", "utc_start": ""}

with open('status.json', 'w') as f:
    json.dump(get_status(), f)
