import cv2

def draw_rectangle_on_image(
    image_path: str,
    output_path: str,
    x1: int,
    y1: int,
    x2: int,
    y2: int
):
    """
    Reads an image from `image_path`, draws a red rectangle using the provided
    coordinates, and saves the edited image to `output_path`.

    Args:
        image_path (str): Path to the input image.
        output_path (str): Path to save the output image.
        x1, y1, x2, y2 (int): The bounding coordinates for the rectangle.
    """
    # Read the image
    image = cv2.imread(image_path)

    # If image is None, the path may be wrong or the image is not readable
    if image is None:
        raise ValueError(f"Could not read the image at {image_path}.")

    # OpenCV expects points as (x, y) format
    # (x1, y1) is the top-left corner, and (x2, y2) is the bottom-right corner
    # color is BGR format: (0, 0, 255) = red
    # thickness=2 means the rectangle border will be 2 pixels thick
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), thickness=2)

    # Save the modified image
    cv2.imwrite(output_path, image)
    print(f"Output image saved to: {output_path}")


if __name__ == "__main__":
#     [
#   {"box_2d": [175, 44, 259, 121], "label": "roblox player head"}
# ]

    # Example usage:
    # Change these to match your rectangle coordinates
    # rect_x1 = 60
    # rect_y1 = 135
    # rect_x2 = 80
    # rect_y2 = 150
    rect_x1 = 72
    rect_y1 = 137
    rect_x2 = 75
    rect_y2 = 140

    # Input and output paths (modify as needed)
    input_image_path = "screenshots/screenshot_0110.png"
    output_image_path = "screenshots/screenshot_0110_out.png"

    # Draw the rectangle
    draw_rectangle_on_image(
        input_image_path,
        output_image_path,
        27, 51, 49, 73
    )