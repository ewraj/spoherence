import os

# Firebase Configuration
FIREBASE_KEY_PATH = "serviceAccountKey.json"
COLLECTION_USERS = "users"
COLLECTION_FRIENDS = "friends"
COLLECTION_JAM_LINKS = "jam_links"
COLLECTION_GROUPS = "groups"

# Spotify Configuration
# Note: Client ID and Secret should ideally be in environment variables
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "your_client_id_here")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "your_client_secret_here")
SPOTIFY_REDIRECT_URI = "http://localhost:8888/callback"
SPOTIFY_SCOPE = "user-read-playback-state user-follow-read"

# App Settings
PRESENCE_CHECK_INTERVAL = 10  # seconds
JAM_LINK_TTL_MINUTES = 30
CLIPBOARD_CHECK_INTERVAL = 0.5  # seconds
