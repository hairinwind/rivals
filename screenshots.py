import pyautogui
import time
import os
import datetime
from AppKit import NSWorkspace, NSApplicationActivateIgnoringOtherApps
from pynput import keyboard
from window import get_window_coordinates_by_title
import threading
import sys  # Required to quit the program

# Global variable to control screenshot capturing
capture_active = False

def capture_screenshots(interval=1, directory="screenshots", window_title=None):
    """Captures screenshots at regular intervals, saving them directly into the specified folder."""
    global capture_active

    os.makedirs(directory, exist_ok=True)
    screenshot_count = 0

    if window_title:
        try:
            window_coordinates = get_window_coordinates_by_title(window_title)
        except Exception as e:
            print(e)
            return

    while capture_active:  # Respect the global capture_active flag
        try:
            if window_title:
                region_tuple = (
                    int(window_coordinates['x']),
                    int(window_coordinates['y']),
                    int(window_coordinates['width']),
                    int(window_coordinates['height'])
                )
                screenshot = pyautogui.screenshot(region=region_tuple)
            else:
                screenshot = pyautogui.screenshot()

            # Generate filename with timestamp and sequence
            timestamp = datetime.datetime.now().strftime("%m%d%H%M")  # Format: MMDDHHMM
            filename = f"screenshot_{timestamp}-{screenshot_count:04d}.png"
            filepath = os.path.join(directory, filename)

            # Save screenshot
            screenshot.save(filepath)
            print(f"Screenshot saved to {filepath}")

            screenshot_count += 1

        except Exception as e:
            print(f"Error capturing or saving screenshot: {e}")

        time.sleep(interval)

def on_press(key):
    """Handle key press events."""
    global capture_active

    try:
        if key.char == 'z':  # Toggle capturing screenshots
            if capture_active:
                capture_active = False
                print("Stopping screenshot capture...")
            else:
                capture_active = True
                print("Starting screenshot capture...")
                # Run capture in a separate thread to avoid blocking the listener
                threading.Thread(target=capture_screenshots, args=(1, "screenshots", "Roblox"), daemon=True).start()
        elif key.char == 'q':  # Quit the program
            print("Quitting the program...")
            sys.exit(0)  # Exit the program
    except AttributeError:
        pass

def main():
    print("Press 'z' to start or stop capturing screenshots.")
    print("Press 'q' to quit the program.")
    
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    main()