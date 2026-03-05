import pyperclip
import re
import time

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
                # This is where we will eventually add the Firebase push logic
            
            last_clip = current_clip
        
        time.sleep(0.5) # Check every half second to keep CPU usage low

if __name__ == "__main__":
    monitor_clipboard()
