import cv2
import numpy as np

def scale_image(image, scale_factor):
    """Scale an image by a given factor."""
    height, width, channels = image.shape
    new_height = int(height * scale_factor)
    new_width = int(width * scale_factor)

    # Create an empty array for the scaled image
    scaled_image = np.zeros((new_height, new_width, channels), dtype=np.uint8)

    # Map pixels from the original image to the scaled image
    for i in range(new_height):
        for j in range(new_width):
            src_x = int(i / scale_factor)
            src_y = int(j / scale_factor)
            scaled_image[i, j] = image[src_x, src_y]

    return scaled_image

def rotate_image(image, angle):
    """Rotate an image by a given angle (in degrees) around its center."""
    angle_rad = np.radians(angle)
    height, width, channels = image.shape
    center_x, center_y = height // 2, width // 2

    # Create an empty array for the rotated image
    rotated_image = np.zeros_like(image)

    for i in range(height):
        for j in range(width):
            # Calculate the source coordinates
            x_shifted = i - center_x
            y_shifted = j - center_y

            src_x = int(center_x + (x_shifted * np.cos(angle_rad) - y_shifted * np.sin(angle_rad)))
            src_y = int(center_y + (x_shifted * np.sin(angle_rad) + y_shifted * np.cos(angle_rad)))

            # Check bounds and assign the pixel value
            if 0 <= src_x < height and 0 <= src_y < width:
                rotated_image[i, j] = image[src_x, src_y]

    return rotated_image

def flip_image(image, flip_axis):
    """
    Flip an image along the specified axis.
    flip_axis = 0 -> Vertical flip
    flip_axis = 1 -> Horizontal flip
    """
    height, width, channels = image.shape
    flipped_image = np.zeros_like(image)

    if flip_axis == 0:  # Vertical flip
        for i in range(height):
            flipped_image[i] = image[height - i - 1]

    elif flip_axis == 1:  # Horizontal flip
        for j in range(width):
            flipped_image[:, j] = image[:, width - j - 1]

    return flipped_image

def main():
    # Load the JPG image
    image = cv2.imread('Exp 2.jpg')  # Replace 'input.jpg' with your image file path
    if image is None:
        print("Error: Could not load image.")
        return

    # Perform operations
    scale_factor = 0.5
    angle = 45  # Angle in degrees

    scaled_image = scale_image(image, scale_factor)
    rotated_image = rotate_image(image, angle)
    flipped_image_vertical = flip_image(image, 0)
    flipped_image_horizontal = flip_image(image, 1)

    # Save results
    cv2.imwrite('scaled_image.jpg', scaled_image)
    cv2.imwrite('rotated_image.jpg', rotated_image)
    cv2.imwrite('flipped_image_vertical.jpg', flipped_image_vertical)
    cv2.imwrite('flipped_image_horizontal.jpg', flipped_image_horizontal)

    print("Operations completed. Check the output files in the working directory.")

if __name__ == "__main__":
    main()
