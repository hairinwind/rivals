from screenshots import capture_screenshot
from local_model import DetectionModel
from mouse_move import move_mouse_to_window
import numpy as np

def getXy(coordinate): 
    """
    Extracts the x and y coordinates from the given input.
    
    Args:
        coordinate (dict): A dictionary containing keys 'x' and 'y'.
    
    Returns:
        tuple: A tuple containing (x, y) coordinates.
    """
    try:
        # Ensure coordinate contains the expected keys
        if 'x' in coordinate and 'y' in coordinate:
            x = coordinate['x']
            y = coordinate['y']
            print(f"Extracted coordinates: x={x}, y={y}")
            return x, y
        else:
            raise KeyError("Coordinate dictionary does not contain 'x' or 'y'.")
    except Exception as e:
        print(f"Error in getXy: {e}")
        return 0, 0  # Return default values if there's an error

def main():
    print("Starting the screenshot capture process...")
    model = DetectionModel()

    print("Attempting to capture a screenshot...")
    roblox_window_title = "Roblox"
    screenshot = capture_screenshot(window_title=roblox_window_title)  # Full screen in this case

    if screenshot:
        # call local_model.py to get the coordination
        screenshot_rgb = screenshot.convert("RGB")
        screenshot_array = np.array(screenshot_rgb)
        coordinate = model.get_detection_coordinates(screenshot_array)
        relative_x, relative_y = getXy(coordinate)
        move_mouse_to_window(roblox_window_title, relative_x, relative_y)
    else:
        print("Failed to capture a screenshot.")

if __name__ == "__main__":
    print("Executing main.py...")
    main()