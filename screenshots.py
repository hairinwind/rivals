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

def save_screenshot(screenshot, directory, screenshot_count):
    """
    Saves the given screenshot with a generated filename based on timestamp and sequence.
    
    Args:
        screenshot (PIL.Image): The screenshot image object.
        directory (str): The directory where screenshots will be saved.
        screenshot_count (int): The current screenshot sequence number.
        
    Returns:
        str: The file path of the saved screenshot.
    """
    timestamp = datetime.datetime.now().strftime("%m%d%H%M")  # Format: MMDDHHMM
    filename = f"screenshot_{timestamp}-{screenshot_count:04d}.png"
    filepath = os.path.join(directory, filename)

    try:
        screenshot.save(filepath)
        print(f"Screenshot saved to {filepath}")
    except Exception as e:
        print(f"Error saving screenshot: {e}")
    return filepath

def capture_screenshot(window_title=None):
    """
    Captures a single screenshot and returns the image.
    
    Args:
        window_title (str): Optional window title to capture a specific region.
        
    Returns:
        PIL.Image: The captured screenshot image.
    """
    print(f"Debug: capture_screenshot called with window_title={window_title}")

    if window_title:
        try:
            print("Debug: Attempting to get window coordinates...")
            window_coordinates = get_window_coordinates_by_title(window_title)
            print(f"Debug: Window coordinates: {window_coordinates}")

            region_tuple = (
                int(window_coordinates['x']),
                int(window_coordinates['y']),
                int(window_coordinates['width']),
                int(window_coordinates['height'])
            )
            print(f"Debug: Capturing region: {region_tuple}")
            screenshot = pyautogui.screenshot(region=region_tuple)
            print("Debug: Region screenshot captured successfully.")
        except Exception as e:
            print(f"Error capturing screenshot: {e}")
            return None
    else:
        print("Debug: Capturing full-screen screenshot...")
        try:
            screenshot = pyautogui.screenshot()
            print("Debug: Full-screen screenshot captured successfully.")
        except Exception as e:
            print(f"Error capturing screenshot: {e}")
            return None

    return screenshot

def capture_screenshots(interval=1, directory="screenshots", window_title=None):
    """
    Captures screenshots at regular intervals, saving them to a directory.
    """
    global capture_active

    os.makedirs(directory, exist_ok=True)
    screenshot_count = 0

    while capture_active:  # Respect the global capture_active flag
        try:
            screenshot = capture_screenshot(window_title)
            if screenshot:
                save_screenshot(screenshot, directory, screenshot_count)
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
    
    # Example of directly using `capture_screenshot`
    screenshot = capture_screenshot()
    if screenshot:
        print("Screenshot captured and accessible in main.")

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    main()