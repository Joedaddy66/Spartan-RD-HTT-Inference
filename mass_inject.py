import csv
import firebase_admin
from firebase_admin import firestore

# Initialize
if not firebase_admin._apps:
    firebase_admin.initialize_app()
db = firestore.client()

def mass_upload(file_path):
    with open(file_path, mode='r') as f:
        reader = csv.DictReader(f)
        batch = db.batch()
        count = 0
        
        for row in reader:
            # Create a new document reference with a random ID
            doc_ref = db.collection('active_leads').document()
            batch.set(doc_ref, row)
            count += 1
            
            # Firestore batch limit is 500
            if count % 500 == 0:
                batch.commit()
                batch = db.batch()
                print(f"✅ Committed {count} leads...")
        
        batch.commit()
        print(f"🚀 Mission Accomplished: {count} leads live in the Nexus.")

mass_upload('leads.csv')
