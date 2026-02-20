import sqlite3
import stripe
import os
from dotenv import load_dotenv

load_dotenv()
stripe.api_key = os.getenv("STRIPE_API_KEY")

def trigger_milestone_payment(company_name):
    conn = sqlite3.connect('nexus.db')
    c = conn.cursor()
    c.execute("SELECT email, potential FROM leads WHERE name=?", (company_name,))
    target = c.fetchone()
    
    if target:
        email, total_val = target
        # Create a "Golden Gate" invoice for the first 10% of the contract
        amount = int(total_val * 0.10 * 100) # $40,000 in cents
        
        invoice = stripe.InvoiceItem.create(
            customer=stripe.Customer.create(email=email, description=company_name).id,
            amount=amount,
            currency="usd",
            description=f"Project Lazarus: 1-in-875M Identification Milestone - {company_name}"
        )
        print(f"💰 INVOICE STAGED: ${amount/100:,.2f} for {company_name}")
        print(f"🔗 TARGET: {email}")

if __name__ == "__main__":
    trigger_milestone_payment("AstraZeneca")
