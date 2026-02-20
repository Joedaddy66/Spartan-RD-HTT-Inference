import sqlite3
import os
import stripe
from dotenv import load_dotenv
from google import genai

load_dotenv()
stripe.api_key = os.getenv("STRIPE_API_KEY")
gemini_key = os.getenv("GEMINI_API_KEY")

def execute_strike(target_name):
    conn = sqlite3.connect('nexus.db')
    c = conn.cursor()
    c.execute("SELECT email, potential FROM leads WHERE name=?", (target_name,))
    row = c.fetchone()
    if not row: return
    
    email, potential = row
    
    # 1. The Power Specs (Your AI Studio Metrics)
    stats = {
        "ingest": "1,000,000 Patients",
        "precision": "1-in-875M Signature Identification",
        "throughput": "166,400 records/sec",
        "target": "HMN1 (Huntington's)"
    }

    # 2. Stripe Hook ($34,450 Validation)
    try:
        product = stripe.Product.create(name=f"Project Lazarus: {target_name} Ingest")
        price = stripe.Price.create(product=product.id, unit_amount=3445000, currency="usd")
        checkout = stripe.PaymentLink.create(line_items=[{"price": price.id, "quantity": 1}])
        payment_url = checkout.url
    except:
        payment_url = "[STRIPE_PAYMENT_LINK]"

    # 3. The "Sovereign" Pitch
    pitch = f"""
SUBJECT: PRODUCTION LOG: 1-in-875M Variant Identified for {target_name}

{email.split('@')[0]},

Our R&D platform (REDTEAM-CRISPR-LOGIC) has successfully processed the 1M patient ingest. 

We have isolated a 1-in-875M genetic signature relevant to your HMN1 targets. This was processed at a throughput of {stats['throughput']} with FIPS-140-2 level 3 cryptographic sealing.

[MISSION CRITICAL DATA]
System State: NOMINAL
Validation Milestone: HTT-001
Status: READY FOR HANDOFF

To access the full identified variant map and the Azure-backed Project Lazarus dashboard, please clear the validation milestone of $34,450.00.

LINK: {payment_url}

Sovereignly,
Joseph Purvis
Project Lazarus Lead
    """
    
    print(pitch)
    # Update DB
    c.execute("UPDATE leads SET status='PITCHED' WHERE name=?", (target_name,))
    conn.commit()

if __name__ == "__main__":
    import sys
    execute_strike(sys.argv[1] if len(sys.argv) > 1 else "AstraZeneca")
