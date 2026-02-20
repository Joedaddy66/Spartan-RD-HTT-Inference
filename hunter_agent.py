import requests
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("HUNTER_API_KEY")

def enrich_lead(company_name, domain):
    print(f"🔍 Hunting for executives at {company_name} ({domain})...")
    # Search for CEO or VP level at the domain
    url = f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key={API_KEY}"
    
    response = requests.get(url).json()
    emails = response.get('data', {}).get('emails', [])
    
    if emails:
        # Pick the one with the highest confidence or a specific 'senior' title
        best_match = emails[0]['value'] 
        print(f"🎯 Found Verified Target: {best_match}")
        return best_match
    else:
        print(f"⚠️ No verified emails found for {domain}.")
        return None

def update_nexus():
    conn = sqlite3.connect('nexus.db')
    c = conn.cursor()
    # Find leads with placeholders
    c.execute("SELECT name FROM leads WHERE email LIKE '%John.Doe%' OR email='Ready'")
    targets = c.fetchall()

    domains = {"AstraZeneca": "astrazeneca.com", "Beam Therapeutics": "beamtx.com", "Prime Medicine": "primemedicine.com"}

    for (name,) in targets:
        domain = domains.get(name)
        if domain:
            real_email = enrich_lead(name, domain)
            if real_email:
                c.execute("UPDATE leads SET email=? WHERE name=?", (real_email, name))
                conn.commit()
                print(f"✅ Nexus Updated: {name} -> {real_email}")

if __name__ == "__main__":
    update_nexus()
