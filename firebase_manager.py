import firebase_admin
from firebase_admin import credentials, firestore
import os
import time
from config import (
    FIREBASE_KEY_PATH, 
    COLLECTION_USERS, 
    COLLECTION_JAM_LINKS, 
    COLLECTION_FRIENDS,
    JAM_LINK_TTL_MINUTES
)

class FirebaseManager:
    def __init__(self):
        self.db = None
        self.current_user_id = None

    def initialize(self):
        """Initializes Firebase Admin SDK."""
        if not os.path.exists(FIREBASE_KEY_PATH):
            print(f"Error: {FIREBASE_KEY_PATH} not found.")
            return False
        
        try:
            cred = credentials.Certificate(FIREBASE_KEY_PATH)
            firebase_admin.initialize_app(cred)
            self.db = firestore.client()
            print("Firebase initialized successfully.")
            return True
        except Exception as e:
            print(f"Failed to initialize Firebase: {e}")
            return False

    def get_or_create_user(self, user_info):
        """Registers the user in Firestore if they don't exist."""
        if not self.db: return
        
        self.current_user_id = user_info['id']
        user_ref = self.db.collection(COLLECTION_USERS).document(self.current_user_id)
        
        doc = user_ref.get()
        if not doc.exists:
            user_ref.set({
                "display_name": user_info.get('display_name'),
                "email": user_info.get('email'),
                "created_at": firestore.SERVER_TIMESTAMP,
                "presence_status": "offline"
            })
            print(f"Created new user profile for {user_info.get('display_name')}")
        else:
            print(f"Welcome back, {user_info.get('display_name')}")

    def update_presence(self, presence_data):
        """Updates the user's presence status in Firestore."""
        if not self.db or not self.current_user_id: return
        
        user_ref = self.db.collection(COLLECTION_USERS).document(self.current_user_id)
        try:
            user_ref.update({
                "presence_status": "online" if presence_data['is_active'] else "idle",
                "current_track": presence_data.get('song_name', ""),
                "current_artist": presence_data.get('artist_name', ""),
                "last_active": firestore.SERVER_TIMESTAMP
            })
        except Exception as e:
            print(f"Error updating presence: {e}")

    def sync_jam_link(self, url, target_group_id=None, privacy_mode="public"):
        """Pushes a Jam link to the cloud pool."""
        if not self.db or not self.current_user_id: return
        
        try:
            expiration = time.time() + (JAM_LINK_TTL_MINUTES * 60)
            data = {
                "url": url,
                "sender_id": self.current_user_id,
                "created_at": firestore.SERVER_TIMESTAMP,
                "expires_at": expiration,
                "privacy": privacy_mode,
                "target_group": target_group_id
            }
            self.db.collection(COLLECTION_JAM_LINKS).add(data)
            print(f"Successfully shared link to {privacy_mode}: {url}")
        except Exception as e:
            print(f"Error syncing link: {e}")

    def listen_for_new_links(self, callback):
        """Sets up a real-time listener for new Jam links."""
        if not self.db: return
        
        links_ref = self.db.collection(COLLECTION_JAM_LINKS).where("expires_at", ">", time.time())
        
        def on_snapshot(col_snapshot, changes, read_time):
            for change in changes:
                if change.type.name == 'ADDED':
                    doc = change.document.to_dict()
                    # Filter: Only trigger for links NOT sent by me
                    if doc['sender_id'] != self.current_user_id:
                        callback(doc)

        links_ref.on_snapshot(on_snapshot)

if __name__ == "__main__":
    # Test initialization
    fm = FirebaseManager()
    fm.initialize()
