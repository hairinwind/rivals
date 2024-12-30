import time
from AppKit import NSWorkspace, NSApplicationActivateIgnoringOtherApps

def get_window_coordinates_by_title(window_title):
    """
    Gets the coordinates of a specified window by its title on macOS using Quartz.
    
    Args:
        window_title (str): The title or a part of the title of the window to locate.

    Returns:
        dict: A dictionary containing the coordinates and dimensions of the window (x, y, width, height).
              Returns None if the window is not found.
    """
    try:
        workspace = NSWorkspace.sharedWorkspace()
        running_apps = workspace.runningApplications()

        for app in running_apps:
            if window_title.lower() in app.localizedName().lower():
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
                    if window_title.lower() in str(owner_name).lower():
                        bounds = window.get('kCGWindowBounds')
                        if bounds:
                            coords = {
                                'x': bounds['X'],
                                'y': bounds['Y'],
                                'width': bounds['Width'],
                                'height': bounds['Height']
                            }
                            print(f"Found window '{window_title}' coordinates: {coords}")
                            return coords
        print(f"Window with title '{window_title}' not found.")
    except Exception as e:
        print(f"Error locating window: {e}")
    return None