from firebase_functions import firestore_fn, options
from firebase_admin import initialize_app, firestore
import google.generativeai as genai
import smtplib, os
from email.mime.text import MIMEText

initialize_app()

@firestore_fn.on_document_created(document="active_leads/{leadId}")
def autonomous_gilded_spear(event: firestore_fn.Event[firestore_fn.DocumentSnapshot | None]) -> None:
    # 1. Grab the Lead Data
    if event.data is None: return
    lead_data = event.data.to_dict()
    
    # 2. Wake up the Brain (Gemini)
    genai.configure(api_key=os.environ.get("GOOGLE_GENERATIVE_AI_API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"Target: {lead_data.get('name')}. Context: CRISPR resonance data. Write a $400k pitch."
    response = model.generate_content(prompt)
    pitch = response.text

    # 3. Launch the Spear (Email)
    try:
        msg = MIMEText(pitch)
        msg['Subject'] = "Strategic Partnership: CRISPR Resonance Breakthrough"
        msg['From'] = os.environ.get("GMAIL_USER")
        msg['To'] = lead_data.get('email')

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(os.environ.get("GMAIL_USER"), os.environ.get("GMAIL_APP_PASSWORD"))
            server.send_message(msg)
        
        # 4. Log the Win
        db = firestore.client()
        db.collection("outreach_logs").add({
            "leadId": event.params["leadId"],
            "status": "Delivered",
            "pitch_summary": pitch[:100]
        })
    except Exception as e:
        print(f"Empire Error: {e}")
