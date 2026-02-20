import sqlite3
import os

def execute_strike(target_name):
    conn = sqlite3.connect('nexus.db')
    c = conn.cursor()
    c.execute("SELECT email, potential FROM leads WHERE name=?", (target_name,))
    row = c.fetchone()
    if not row: return
    
    email = row[0]
    
    # Live Infrastructure Links
    dashboard_url = "https://integer-resonance-crispr-oc8grgr22-joseph-e-purvis-projects.vercel.app"
    stripe_link = "https://buy.stripe.com/test_6oEbL00Xf9v090I3cc" # Placeholder for your live link

    if "Tune" in target_name:
        subject = "Precision HBV Validation for Tune-401 — Congratulations on $175M Series B"
        body = f"Derek,\n\nCongratulations on the momentum for the Tune-401 Hepatitis B program. Our Spartan RGA platform has isolated a 1-in-875M genetic resonance variant relevant to your HBV epigenetic silencing work.\n\nVIEW DASHBOARD: {dashboard_url}\nMILESTONE PAYMENT: {stripe_link}"
    elif "Intellia" in target_name:
        subject = "MAGNITUDE-2 Liver Safety — Pipeline Guardrails via 1M Patient Ingest"
        body = f"Birgit,\n\nCongratulations on the FDA lift for MAGNITUDE-2. Our REDTEAM-CRISPR-LOGIC suite has ingested 1M patient records to identify off-target enzyme elevations—a liver safety guardrail ready for your Phase 3 resumption.\n\nVIEW DASHBOARD: {dashboard_url}\nMILESTONE PAYMENT: {stripe_link}"
    
    print(f"\n--- {target_name} DISPATCH ---")
    print(f"To: {email}")
    print(f"Subject: {subject}")
    print(f"\n{body}\n")

if __name__ == "__main__":
    import sys
    execute_strike(sys.argv[1])
