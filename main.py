import time
import threading
from pynput import keyboard
from screenshots import capture_screenshot
from local_model import DetectionModel
from mouse_move import move_mouse_to_window
import numpy as np

# Global variables to manage the capturing state
capture_active = False
program_running = True
capture_interval = 1.0  # Default interval in seconds

def getXy(coordinate):
    """
    Extracts the x and y coordinates from the given input.
    
    Args:
        coordinate (Detections): A Detections object containing bounding box information.
    
    Returns:
        tuple: A tuple containing (x, y) coordinates of the center of the bounding box.
    """
    try:
        if coordinate and "xyxy" in coordinate and coordinate["xyxy"] is not None:
            # Calculate the center of the bounding box
            xyxy = coordinate["xyxy"][0]  # Assuming single detection for simplicity
            x_center = (xyxy[0] + xyxy[2]) / 2  # Average of x_min and x_max
            y_center = (xyxy[1] + xyxy[3]) / 2  # Average of y_min and y_max
            print(f"Extracted coordinates: x_center={x_center}, y_center={y_center}")
            return x_center, y_center
        else:
            raise ValueError("Coordinate does not contain 'xyxy' or is empty.")
    except Exception as e:
        print(f"Error in getXy: {e}")
        return 0, 0  # Return default values if there's an error

def capture_screen_loop(interval):
    """
    Continuously captures the screen at the given interval while capture_active is True.
    """
    model = DetectionModel()
    roblox_window_title = "Roblox"

    while program_running:
        if capture_active:
            print("Attempting to capture a screenshot...")
            screenshot = capture_screenshot(window_title=roblox_window_title)  # Full screen in this case
            if screenshot:
                screenshot_rgb = screenshot.convert("RGB")
                screenshot_array = np.array(screenshot_rgb)
                x, y = model.get_position(screenshot_array)
                if x is not None: 
                    print("found target: ", x, y)
                    move_mouse_to_window(roblox_window_title, x, y)
            else:
                print("Failed to capture a screenshot.")
        time.sleep(interval)

def on_key_press(key):
    """
    Handles key press events for controlling screen capture and program quitting.
    """
    global capture_active, program_running

    try:
        if key.char == 'z':
            capture_active = not capture_active
            if capture_active:
                print("Started screen capture.")
            else:
                print("Stopped screen capture.")
        elif key.char == 'q':
            print("Exiting program...")
            program_running = False
            return False  # Stops the keyboard listener
    except AttributeError:
        pass

def main():
    global capture_interval

    print("Starting the program...")

    # Allow the user to specify the capture interval
    try:
        interval_input = input("Enter capture interval in seconds (default is 1.0): ").strip()
        if interval_input:
            capture_interval = float(interval_input)
            print(f"Capture interval set to {capture_interval} seconds.")
        else:
            print("Using default capture interval of 1.0 seconds.")
    except ValueError:
        print("Invalid input. Using default capture interval of 1.0 seconds.")

    capture_thread = threading.Thread(target=capture_screen_loop, args=(capture_interval,), daemon=True)
    capture_thread.start()

    print("Listening for key presses ('z' to start/stop capture, 'q' to quit)...")
    with keyboard.Listener(on_press=on_key_press) as listener:
        listener.join()

if __name__ == "__main__":
    print("Executing main.py...")
    main()