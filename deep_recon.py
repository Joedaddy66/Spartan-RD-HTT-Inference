import requests
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("HUNTER_API_KEY")

def deep_hunt(domain):
    # Filters for the 'Decision Makers' (VP/Chief/Director)
    url = f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key={API_KEY}&seniority=senior,executive&department=executive,it"
    
    try:
        res = requests.get(url).json()
        emails = res.get('data', {}).get('emails', [])
        
        for e in emails:
            # Prioritize R&D, Data, and Tech leaders
            pos = (e.get('position') or "").lower()
            if any(k in pos for k in ['data', 'r&d', 'chief', 'scientific', 'tech']):
                return e['value'], e['position']
        
        # Fallback to the first executive found
        if emails: return emails[0]['value'], emails[0]['position']
    except Exception as e:
        print(f"⚠️ Error scouting {domain}: {e}")
    return None, None

def mass_enrich():
    conn = sqlite3.connect('nexus.db')
    c = conn.cursor()
    
    # High-Value 2026 Targets
    targets = [
        ("Gilead", "gilead.com"), ("Novartis", "novartis.com"), 
        ("Tune Therapeutics", "tunetx.com"), ("SpliceBio", "splice.bio"),
        ("Beam Therapeutics", "beamtx.com"), ("Intellia", "intelliatx.com")
    ]
    
    for name, domain in targets:
        print(f"📡 Deep Recon: {name}...")
        email, title = deep_hunt(domain)
        if email:
            c.execute("INSERT OR REPLACE INTO leads (name, email, status, potential) VALUES (?, ?, 'Ready', 400000.0)", (name, email))
            print(f"🎯 LOCKED: {email} ({title})")
    
    conn.commit()
    print("\n🛡️ RECON COMPLETE: Nexus.db is updated with high-value targets.")

if __name__ == "__main__":
    mass_enrich()
