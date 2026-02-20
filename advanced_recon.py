import requests
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("HUNTER_API_KEY")

# Target High-Value 2026 Tiers
biotech_targets = [
    {"name": "Gilead Sciences", "domain": "gilead.com"},
    {"name": "Novartis", "domain": "novartis.com"},
    {"name": "Intellia Therapeutics", "domain": "intelliatx.com"},
    {"name": "CRISPR Therapeutics", "domain": "crisprtx.com"},
    {"name": "Regeneron", "domain": "regeneron.com"}
]

def hunt_executives(company, domain):
    print(f"📡 Reconnaissance on {company}...")
    # Using the 'Decision Makers' filter via API
    url = f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key={API_KEY}&seniority=senior,executive"
    
    res = requests.get(url).json()
    emails = res.get('data', {}).get('emails', [])
    
    # Filter for R&D or Data Officers
    for e in emails:
        title = (e.get('position') or "").lower()
        if any(keyword in title for keyword in ['r&d', 'data', 'scientific', 'tech', 'chief']):
            print(f"🎯 TARGET LOCKED: {e['value']} ({e['position']})")
            return e['value'], e['position']
    return None, None

def update_nexus():
    conn = sqlite3.connect('nexus.db')
    c = conn.cursor()
    
    for target in biotech_targets:
        email, title = hunt_executives(target['name'], target['domain'])
        if email:
            c.execute("INSERT OR REPLACE INTO leads (name, email, status, potential) VALUES (?, ?, 'Ready', 400000.0)", 
                      (target['name'], email))
            print(f"✅ Nexus Updated: {target['name']} -> {email}")
    conn.commit()

if __name__ == "__main__":
    update_nexus()
