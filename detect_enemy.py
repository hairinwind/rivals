import pyautogui
import time
import os
import cv2
import numpy as np
import Quartz
from AppKit import NSWorkspace, NSApplicationActivateIgnoringOtherApps
from pynput import mouse
from pynput.mouse import Button, Listener

def capture_screenshots(duration=10, interval=1, directory="screenshots", window_title=None):
    """Captures screenshots at regular intervals for a specified duration,
       BUT only saves them if the left mouse button is clicked.
    """
    os.makedirs(directory, exist_ok=True)
    os.makedirs(os.path.join(directory, "archive"), exist_ok=True)
    start_time = time.time()
    screenshot_count = 0

    # If you need window coordinates
    if window_title:
        try:
            window_coordinates = get_window_coordinates(window_title)
        except Exception as e:
            print(e)
            return

    while time.time() - start_time < duration:
        try:
            # Always capture a screenshot in memory (but only save it if left_click_flag = True)
            if window_title and window_coordinates:
                region_tuple = (
                    int(window_coordinates['x']),
                    int(window_coordinates['y']),
                    int(window_coordinates['width']),
                    int(window_coordinates['height'])
                )
                screenshot = pyautogui.screenshot(region=region_tuple)
            else:
                screenshot = pyautogui.screenshot()

            # Check if an enemy is detected in the screenshot
            enemy_detected = detect_enemy_in_screenshot(screenshot)

            # ONLY SAVE if user clicked the left mouse button
            if left_click_flag:
                left_click_flag = False  # Reset flag
                screenshot_count += 1
                filename = f"screenshot_{screenshot_count:04d}.png"
                
                if enemy_detected:
                    filepath = os.path.join(directory, filename)
                else:
                    filepath = os.path.join(directory, "archive", filename)

                screenshot.save(filepath)
                print(f"Screenshot saved to {filepath}")

        except Exception as e:
            print(f"Error capturing or saving screenshot: {e}")

        time.sleep(interval)

def detect_enemy_in_screenshot(screenshot):
    """Detects if an enemy is present in the screenshot."""
    # Convert the PyAutoGUI screenshot to an OpenCV image
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

    if img is None:
        print(f"Error: Could not convert screenshot to image")
        return False

    _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w > 50 and h > 50 and 0.5 < w / h < 2:  # Basic filtering based on size and aspect ratio
            return True  # Enemy detected

    return False  # No enemy detected

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
                # Removed decode() since the string is already decoded
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

# Example usage: Capture screenshots from the "Roblox" window for 30 seconds with a 1-second interval
capture_screenshots(duration=120, interval=0.5, window_title="Roblox")
