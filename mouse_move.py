from window import get_window_coordinates_by_title
from AppKit import NSScreen
from pynput.mouse import Controller

import pyautogui

def get_scaling_factor():
    """
    Gets the scaling factor of the primary display using NSScreen.
    Returns:
        float: The scaling factor (e.g., 2.0 for Retina displays, 1.0 for standard).
    """
    primary_screen = NSScreen.mainScreen()
    scaling_factor = primary_screen.backingScaleFactor()
    return scaling_factor

def move_mouse_with_pynput(x, y):
    """
    Moves the mouse to the specified absolute screen coordinates using pynput.

    Args:
        x (int): The x-coordinate on the screen.
        y (int): The y-coordinate on the screen.
    """
    mouse = Controller()
    mouse.position = (x, y)  # Move to absolute screen coordinates
    print(f"Mouse moved to {mouse.position}")

def move_mouse_to_window(title, x, y, duration=0):
    """
    Move the mouse to a specific position relative to the top-left corner of a window.

    Args:
        title (str): The title of the window to find.
        x (int): The x-coordinate relative to the window's left corner.
        y (int): The y-coordinate relative to the window's top corner.
    """
    try:
        scaling_factor = get_scaling_factor()
        # Get window coordinates
        window_coords = get_window_coordinates_by_title(title)
        if not window_coords:
            print(f"Window with title '{title}' not found.")
            return

        # Calculate the absolute screen coordinates
        screen_x = window_coords['x'] + x/scaling_factor
        screen_y = window_coords['y'] + y/scaling_factor

        # Move the mouse
        # pyautogui.moveTo(screen_x, screen_y, duration=duration)
        move_mouse_with_pynput(screen_x, screen_y)
        
        print(f"Mouse moved to ({screen_x}, {screen_y}) relative to window '{title}'.")
    except Exception as e:
        print(f"An error occurred: {e}")


# Example usage
if __name__ == "__main__":
    window_title = "Roblox"  # Replace with the window title
    relative_x = 1800  # Replace with desired x-coordinate
    relative_y = 1300 # Replace with desired y-coordinate

    move_mouse_to_window(window_title, relative_x, relative_y, duration=0.5)