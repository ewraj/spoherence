import pyperclip
import re
import time
from config import CLIPBOARD_CHECK_INTERVAL

class ClipboardMonitor:
    def __init__(self):
        # The Regex pattern for Spotify short links
        self.JAM_PATTERN = r"https://spotify\.link/[a-zA-Z0-9]+"
        self.last_clip = ""
        self.privacy_mode = "public" # Default
        self.target_group = None

    def set_privacy(self, mode, group_id=None):
        self.privacy_mode = mode
        self.target_group = group_id
        print(f"Privacy set to: {mode} (Group: {group_id})")

    def watch(self, on_capture_callback):
        """Monitors clipboard in a loop. Should be run in a background thread."""
        while True:
            try:
                current_clip = pyperclip.paste()
                
                # Only process if the clipboard content actually changed
                if current_clip != self.last_clip:
                    match = re.search(self.JAM_PATTERN, current_clip)
                    if match:
                        jam_url = match.group(0)
                        print(f"Captured: {jam_url}")
                        # Filter check (handled by UI state)
                        if self.privacy_mode != "stealth":
                            on_capture_callback(jam_url, self.target_group, self.privacy_mode)
                    
                    self.last_clip = current_clip
                
                time.sleep(CLIPBOARD_CHECK_INTERVAL)
            except Exception as e:
                print(f"Clipboard monitoring error: {e}")
                time.sleep(1)

if __name__ == "__main__":
    def test_cb(url, group, privacy):
        print(f"Callback triggered: {url} | {group} | {privacy}")
        
    monitor = ClipboardMonitor()
    monitor.watch(test_cb)
