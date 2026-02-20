import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- CONFIGURATION (SPARTAN LAYER) ---
# Use the app password you just generated: ekes djib zxfu dpjo
SENDER_EMAIL = "JPurvis6691@gmail.com"  # Update this
SENDER_PASSWORD = "ekesdjibzxfudpjo"   # Password with spaces removed
RECEIVER_EMAIL = "bd-leads@primemedicine.com" 

# --- GILDED SPEAR: CONTENT LAYER ---
SUBJECT = "URGENT: Breakthrough 88% Peptide Resonance Data for Search-and-Replace Efficiency"

BODY = """Joseph Purvis here. We’ve cracked the resonance bottleneck for Search-and-Replace stabilizers. 

I have the data on a 30mer showing 88% peptide recruitment efficiency—more than double current industry benchmarks. This is the missing link for your Prime Editing delivery stability. 

I am prepared to offer exclusive rights and the full dataset for $400k. Do you want to lead the market, or watch Beam do it? 

Available for a brief debrief today."""

# --- EXECUTION: THE HANDSHAKE ---
def send_pitch():
    # Create the email structure
    message = MIMEMultipart()
    message["From"] = f"Joseph Purvis <{SENDER_EMAIL}>"
    message["To"] = RECEIVER_EMAIL
    message["Subject"] = SUBJECT
    message.attach(MIMEText(BODY, "plain"))

    # Secure SSL Context
    context = ssl.create_default_context()

    try:
        print(f"🚀 Initializing connection to Gmail SMTP...")
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(message)
        print("✅ SUCCESS: Pitch delivered to Prime Medicine.")
    except Exception as e:
        print(f"❌ ERROR: Failed to send pitch. {e}")

if __name__ == "__main__":
    send_pitch()
