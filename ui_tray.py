import pystray
from PIL import Image, ImageDraw
import webbrowser
from plyer import notification
import threading

class TrayApp:
    def __init__(self, on_privacy_change, on_quit):
        self.icon = None
        self.on_privacy_change = on_privacy_change
        self.on_quit = on_quit
        self.is_running = True

    def create_image(self, color):
        # Generate a simple icon for the tray (Spotify green or status color)
        image = Image.new('RGB', (64, 64), color)
        dc = ImageDraw.Draw(image)
        dc.rectangle((16, 16, 48, 48), fill="black")
        return image

    def setup_tray(self):
        menu = pystray.Menu(
            pystray.MenuItem("Status: Active", lambda: None, enabled=False),
            pystray.MenuItem("Privacy", pystray.Menu(
                pystray.MenuItem("Public", lambda: self.on_privacy_change("public")),
                pystray.MenuItem("Stealth", lambda: self.on_privacy_change("stealth")),
                pystray.MenuItem("Better Half Only", lambda: self.on_privacy_change("private", "better_half"))
            )),
            pystray.MenuItem("Quit", self.stop)
        )
        
        self.icon = pystray.Icon("Spoherence", self.create_image("green"), "Spoherence", menu)
        self.icon.run()

    def show_notification(self, sender_name, url):
        """Shows a desktop notification for a new Jam link."""
        notification.notify(
            title="SPOHERENCE: New Jam!",
            message=f"{sender_name} just shared a Jam link! Click to join.",
            app_name="Spoherence",
            timeout=10
        )
        # In a more advanced version, we'd handle the 'on_click' to call webbrowser.open(url)
        # For now, we'll log it or use a simple timer if the OS supports it.

    def stop(self, icon=None, item=None):
        self.is_running = False
        if self.icon:
            self.icon.stop()
        self.on_quit()

if __name__ == "__main__":
    def dummy_privacy(m, g=None): print(f"Mode changed to {m}")
    def dummy_quit(): print("Quitting...")
    
    app = TrayApp(dummy_privacy, dummy_quit)
    app.setup_tray()
