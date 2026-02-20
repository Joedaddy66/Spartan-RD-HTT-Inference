import smtplib
import sqlite3
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

def send_strike(target_name):
    sender = "jpurvis6691@gmail.com"
    # This must be the 16-character App Password (e.g., "xxxx xxxx xxxx xxxx")
    password = os.getenv("GMAIL_APP_PASSWORD") 
    
    if not password:
        print("❌ ERROR: GMAIL_APP_PASSWORD not found in environment.")
        return

    conn = sqlite3.connect('nexus.db')
    c = conn.cursor()
    c.execute("SELECT email FROM leads WHERE name=?", (target_name,))
    row = c.fetchone()
    
    if not row:
        print(f"❌ ERROR: No lead found for {target_name}")
        return
        
    recipient = row[0]
    
    # Customizing hooks based on target
    if "Tune" in target_name:
        subject = "Precision HBV Validation for Tune-401 — Congratulations on $175M Series B"
        body = "Derek,\n\nCongratulations on the Tune-401 momentum. Our Spartan RGA platform has identified the 1-in-875M resonance variant for your HBV silencing targets.\n\nView results: https://integer-resonance-crispr.vercel.app\nMilestone Invoice: https://buy.stripe.com/test_6oEbL00Xf9v090I3cc"
    elif "Intellia" in target_name:
        subject = "MAGNITUDE-2 Liver Safety — Pipeline Guardrails via 1M Patient Ingest"
        body = "Birgit,\n\nCongrats on the FDA lift. We've mapped the 1M patient liver safety guardrail for your Phase 3 resumption.\n\nView results: https://integer-resonance-crispr.vercel.app\nMilestone Invoice: https://buy.stripe.com/test_6oEbL00Xf9v090I3cc"
    else:
        print(f"❌ ERROR: No specific pitch template for {target_name}")
        return

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender, password)
            server.sendmail(sender, recipient, msg.as_string())
        print(f"🚀 DISPATCH SUCCESS: {target_name} ({recipient}) has been struck.")
        c.execute("UPDATE leads SET status='PITCHED' WHERE name=?", (target_name,))
        conn.commit()
    except Exception as e:
        print(f"❌ DISPATCH FAILED for {target_name}: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        send_strike(sys.argv[1])
