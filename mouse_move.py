from window import get_window_coordinates_by_title
import pyautogui

def move_mouse_to_window(title, x, y, duration=0):
    """
    Move the mouse to a specific position relative to the top-left corner of a window.

    Args:
        title (str): The title of the window to find.
        x (int): The x-coordinate relative to the window's left corner.
        y (int): The y-coordinate relative to the window's top corner.
    """
    try:
        # Get window coordinates
        window_coords = get_window_coordinates_by_title(title)
        if not window_coords:
            print(f"Window with title '{title}' not found.")
            return

        # Calculate the absolute screen coordinates
        screen_x = window_coords['x'] + x
        screen_y = window_coords['y'] + y

        # Move the mouse
        pyautogui.moveTo(screen_x, screen_y, duration=duration)
        # Visual feedback: simulate a click
        pyautogui.click()
        print(f"Mouse moved to ({screen_x}, {screen_y}) relative to window '{title}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    window_title = "Roblox"  # Replace with the window title
    relative_x = 400  # Replace with desired x-coordinate
    relative_y = 400  # Replace with desired y-coordinate

    move_mouse_to_window(window_title, relative_x, relative_y, duration=0.5)