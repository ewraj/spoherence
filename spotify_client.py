import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI, SPOTIFY_SCOPE

class SpotifyClient:
    def __init__(self):
        self.sp = None
        self.auth_manager = SpotifyOAuth(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            redirect_uri=SPOTIFY_REDIRECT_URI,
            scope=SPOTIFY_SCOPE,
            open_browser=True
        )

    def authenticate(self):
        """Initializes the Spotify client with OAuth."""
        try:
            self.sp = spotipy.Spotify(auth_manager=self.auth_manager)
            user_info = self.sp.current_user()
            print(f"Authenticated as Spotify user: {user_info['display_name']}")
            return user_info
        except Exception as e:
            print(f"Spotify Authentication failed: {e}")
            return None

    def get_presence_data(self):
        """Returns the current playback state."""
        if not self.sp:
            return None
        
        try:
            playback = self.sp.current_playback()
            if playback and playback.get('is_playing'):
                track = playback['item']
                return {
                    "is_active": True,
                    "song_name": track['name'],
                    "artist_name": track['artists'][0]['name'],
                    "last_updated": time.time()
                }
            return {"is_active": False, "last_updated": time.time()}
        except Exception as e:
            print(f"Error fetching playback state: {e}")
            return None

    def get_social_graph(self):
        """Fetches followers and following IDs."""
        if not self.sp:
            return []
        
        try:
            # Note: Spotify API's 'following' is easier than 'followers' due to privacy
            following = self.sp.current_user_followed_users(type='artist', limit=50) # Example
            # In a real app, we'd iterate through user following list if the scope allows
            return [user['id'] for user in following['artists']['items']] # Simplified for now
        except Exception as e:
            print(f"Error fetching social graph: {e}")
            return []

if __name__ == "__main__":
    # Quick test
    client = SpotifyClient()
    if client.authenticate():
        print(client.get_presence_data())
