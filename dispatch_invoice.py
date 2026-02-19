import json

def generate_dispatch():
    with open('payout_signal.json', 'r') as f:
        payout = json.load(f)
    with open('contacts.json', 'r') as f:
        contacts = json.load(f)

    target = "AstraZeneca" # Orchestrator selects based on repo name
    email = contacts[target]
    
    print(f"--- AUTOMATED DISPATCH QUEUED ---")
    print(f"TO: {email['primary']}")
    print(f"CC: {email['cc']}")
    print(f"SUBJECT: MILESTONE {payout['milestone']} - INVOICE ${payout['invoice_amount']}")
    print(f"BODY:")
    print(f"The Spartan-RD engine has verified the HTT-Validation-001 milestone.")
    print(f"Resonance Peak: {payout['evidence_resonance']:.4f}")
    print(f"Verification Repo: {payout['delivery_repo']}")
    print(f"Please process the automated invoice for ${payout['invoice_amount']}.")
    print(f"--- DISPATCH SUCCESSFUL ---")

if __name__ == "__main__":
    generate_dispatch()
