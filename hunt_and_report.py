import requests
import json
import os
import random

WEBHOOK_URL = "https://discord.com/api/webhooks/1474155341754273877/79gRJoESAGb5MbkINhELDsI3xKHajdaoQbVLS6aiMoiVGq_dRe33IRB67KXaSn_Wl4Ym"
LEADS_FILE = "active_leads.json"

def hunt():
    leads = [
        {"name": "Beam Therapeutics", "value": 250000, "target": "Base Editing"},
        {"name": "Prime Medicine", "value": 400000, "target": "Search-and-Replace"},
        {"name": "Scribe Therapeutics", "value": 300000, "target": "CasX Platform"}
    ]
    target = random.choice(leads)
    
    # Update the Local JSON Database
    current_data = []
    if os.path.exists(LEADS_FILE):
        with open(LEADS_FILE, 'r') as f:
            current_data = json.load(f)
    
    current_data.append(target)
    with open(LEADS_FILE, 'w') as f:
        json.dump(current_data, f)

    # Calculate Total Pipeline
    total_pipeline = sum(item['value'] for item in current_data)

    payload = {
        "embeds": [{
            "title": "🎯 TARGET_ACQUIRED",
            "description": f"New lead identified. Total Pipeline: **${total_pipeline:,}**",
            "color": 15548997,
            "fields": [
                {"name": "Entity", "value": target['name'], "inline": True},
                {"name": "Sector", "value": target['target'], "inline": True}
            ]
        }]
    }
    requests.post(WEBHOOK_URL, json=payload)
    print(f"✅ Pipeline Updated: ${total_pipeline}")

if __name__ == "__main__":
    hunt()
