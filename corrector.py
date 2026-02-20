import firebase_admin
from firebase_admin import firestore
# Import the Filter objects for 2026 compatibility
from google.cloud.firestore_v1.base_query import FieldFilter 
import os
import time

os.environ["GOOGLE_CLOUD_PROJECT"] = "srol-spartan-research"
if not firebase_admin._apps:
    firebase_admin.initialize_app()
db = firestore.client()

def auto_correct():
    # Modernized 2026 Query Syntax
    query = db.collection('active_leads').where(
        filter=FieldFilter("status", "in", ["Injected", "Unknown", "Pending"])
    )
    
    docs = query.get()
    
    if not docs:
        return

    print(f"🛠️  Found {len(docs)} ghost leads. Standardizing to 'Ready'...")
    batch = db.batch()
    for doc in docs:
        batch.update(doc.reference, {"status": "Ready"})
    batch.commit()
    print("✅ Standardization complete.")

if __name__ == "__main__":
    print("🛡️ Corrector Agent: Monitoring for ghost states...")
    while True:
        auto_correct()
        time.sleep(3600)
