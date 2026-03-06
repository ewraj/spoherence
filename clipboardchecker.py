import pyperclip
import re
import time
import firebase_sync

# The Regex pattern for Spotify short links
JAM_PATTERN = r"https://spotify\.link/[a-zA-Z0-9]+"

def monitor_clipboard():
    last_clip = ""
    print("Watching for Jam links... (Ctrl+C to stop)")
    
    while True:
        current_clip = pyperclip.paste()
        
        # Only process if the clipboard content actually changed
        if current_clip != last_clip:
            match = re.search(JAM_PATTERN, current_clip)
            if match:
                jam_url = match.group(0)
                print(f"Captured: {jam_url}")
                # Sync captured link to Firebase
                firebase_sync.sync_jam_link(jam_url)
            
            last_clip = current_clip
        
        time.sleep(0.5) # Check every half second to keep CPU usage low



if __name__ == "__main__":
    monitor_clipboard()
