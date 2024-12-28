import pyautogui
import time
import os
import numpy as np
from AppKit import NSWorkspace, NSApplicationActivateIgnoringOtherApps
from pynput import keyboard

# Global variable to control screenshot capturing
capture_active = False

def capture_screenshots(interval=1, directory="screenshots", window_title=None):
    """Captures screenshots at regular intervals, saving them directly into the specified folder."""
    global capture_active

    os.makedirs(directory, exist_ok=True)
    screenshot_count = 0

    if window_title:
        try:
            window_coordinates = get_window_coordinates(window_title)
        except Exception as e:
            print(e)
            return

    while capture_active:
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

            screenshot_count += 1
            filename = f"screenshot_{screenshot_count:04d}.png"
            filepath = os.path.join(directory, filename)

            screenshot.save(filepath)
            print(f"Screenshot saved to {filepath}")

        except Exception as e:
            print(f"Error capturing or saving screenshot: {e}")

        time.sleep(interval)

def get_window_coordinates(window_title):
    """Gets the coordinates of the specified window on macOS using Quartz."""
    workspace = NSWorkspace.sharedWorkspace()
    running_apps = workspace.runningApplications()
    
    for app in running_apps:
        if "roblox" in app.localizedName().lower():
            app.activateWithOptions_(NSApplicationActivateIgnoringOtherApps)
            time.sleep(0.5)
            
            from Quartz import (
                CGWindowListCopyWindowInfo,
                kCGWindowListOptionOnScreenOnly,
                kCGNullWindowID
            )
            
            window_list = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, kCGNullWindowID)
            for window in window_list:
                owner_name = window.get('kCGWindowOwnerName', '')
                if "roblox" in str(owner_name).lower():
                    bounds = window.get('kCGWindowBounds')
                    if bounds:
                        coords = {
                            'x': bounds['X'],
                            'y': bounds['Y'],
                            'width': bounds['Width'],
                            'height': bounds['Height']
                        }
                        print(f"Found Roblox window coordinates: {coords}")
                        return coords
    return None

def on_press(key):
    """Handle key press events."""
    global capture_active

    try:
        if key.char == 'z':  # Start capturing screenshots
            if not capture_active:
                capture_active = True
                print("Starting screenshot capture...")
                capture_screenshots(interval=0.5, window_title="Roblox")  # Start capture
        elif key.char == 'p':  # Stop capturing screenshots
            capture_active = False
            print("Stopping screenshot capture...")
    except AttributeError:
        pass

def main():
    print("Press 'z' to start capturing screenshots.")
    print("Press 'p' to stop capturing screenshots.")
    
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    main()