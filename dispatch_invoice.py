import json
import stripe
import os

# 1. Financial Clearance
stripe.api_key = os.environ.get("STRIPE_API_KEY")

def generate_dispatch():
    with open('payout_signal.json', 'r') as f:
        payout = json.load(f)
    with open('contacts.json', 'r') as f:
        contacts = json.load(f)

    target = "AstraZeneca"
    client_email = contacts[target]['primary']

    # 2. CREATE THE REAL STRIPE INVOICE
    # (First, we find or create the customer in Stripe)
    customer = stripe.Customer.create(email=client_email, name=target)
    
    invoice = stripe.Invoice.create(
        customer=customer.id,
        auto_advance=True, # Automatically attempts to charge/send
        collection_method="send_invoice",
        days_until_due=7,
    )

    stripe.InvoiceItem.create(
        customer=customer.id,
        invoice=invoice.id,
        amount=int(payout['invoice_amount'] * 100), # Cents
        currency="usd",
        description=f"Milestone {payout['milestone']} - Resonance: {payout['evidence_resonance']}",
    )

    # 3. Finalize and Send
    final_invoice = stripe.Invoice.finalize_invoice(invoice.id)
    
    print(f"--- 🛡️ DISPATCH SUCCESSFUL ---")
    print(f"Invoice Sent to: {client_email}")
    print(f"Payment Link: {final_invoice.hosted_invoice_url}")
    print(f"==============================")

if __name__ == "__main__":
    generate_dispatch()
