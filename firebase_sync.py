import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
import time

# Path to your Firebase service account key
KEY_PATH = "serviceAccountKey.json"

db = None

def initialize_firebase():
    global db
    if not os.path.exists(KEY_PATH):
        print(f"Error: {KEY_PATH} not found. Firebase sync is disabled.")
        return False
    
    try:
        cred = credentials.Certificate(KEY_PATH)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("Firebase initialized successfully.")
        return True
    except Exception as e:
        print(f"Failed to initialize Firebase: {e}")
        return False

def sync_jam_link(url):
    global db
    if db is None:
        if not initialize_firebase():
            return
        
    try:
        data = {
            "url": url,
            "timestamp": firestore.SERVER_TIMESTAMP,
            "captured_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        # Pushing to a 'jam_links' collection
        db.collection("jam_links").add(data)
        print(f"Successfully synced to Firebase: {url}")
    except Exception as e:
        print(f"Error syncing to Firebase: {e}")

if __name__ == "__main__":
    # Test function
    print("Testing Firebase sync...")
    sync_jam_link("https://spotify.link/test-link")
