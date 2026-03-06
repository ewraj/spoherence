import threading
import time
import sys
from spotify_client import SpotifyClient
from firebase_manager import FirebaseManager
from clipboard_monitor import ClipboardMonitor
from ui_tray import TrayApp
from config import PRESENCE_CHECK_INTERVAL

class SpoherenceApp:
    def __init__(self):
        self.spotify = SpotifyClient()
        self.firebase = FirebaseManager()
        self.clipboard = ClipboardMonitor()
        self.tray = TrayApp(self.on_privacy_change, self.on_quit)
        
        self.user_info = None
        self.is_active = True

    def on_privacy_change(self, mode, group_id=None):
        self.clipboard.set_privacy(mode, group_id)

    def on_quit(self):
        print("Shutting down Spoherence...")
        self.is_active = False
        sys.exit(0)

    def presence_loop(self):
        """Polls Spotify and updates Firebase presence every 10s."""
        while self.is_active:
            presence_data = self.spotify.get_presence_data()
            if presence_data:
                self.firebase.update_presence(presence_data)
            time.sleep(PRESENCE_CHECK_INTERVAL)

    def on_jam_captured(self, url, group_id, privacy):
        """Callback for clipboard monitor."""
        self.firebase.sync_jam_link(url, group_id, privacy)

    def on_new_link_received(self, doc):
        """Callback for Firebase link listener."""
        # Here we'd look up the sender's name from Firebase for a better notification
        sender_id = doc.get('sender_id', 'Someone')
        self.tray.show_notification(sender_id, doc['url'])

    def run(self):
        # 1. Initialize Firebase
        if not self.firebase.initialize():
            return

        # 2. Authenticate Spotify
        self.user_info = self.spotify.authenticate()
        if not self.user_info:
            return

        # 3. Register user in Firestore
        self.firebase.get_or_create_user(self.user_info)

        # 4. Start Background Threads
        
        # Thread A: Presence Polling
        threading.Thread(target=self.presence_loop, daemon=True).start()
        
        # Thread B: Clipboard Monitoring
        threading.Thread(target=self.clipboard.watch, args=(self.on_jam_captured,), daemon=True).start()
        
        # Thread C: Listen for incoming links
        self.firebase.listen_for_new_links(self.on_new_link_received)

        # 5. Start Tray UI (Main Thread)
        print("Spoherence is running in the system tray.")
        self.tray.setup_tray()

if __name__ == "__main__":
    app = SpoherenceApp()
    app.run()
