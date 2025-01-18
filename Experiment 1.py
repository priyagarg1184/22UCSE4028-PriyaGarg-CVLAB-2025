import cv2
from skimage import io
import numpy as np
#To open webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open the webcam.")
    exit()

print("Press 'Space' to capture an image and 'ESC' to exit.")

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture image.")
        break

    # Display the captured frame
    cv2.imshow('Webcam', frame)

    # Wait for a key press
    key = cv2.waitKey(1)

    if key == 27:  
        break
    elif key == 32:  
        # Convert the image from BGR to RGB format
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        num_pixels = image_rgb.shape[0] * image_rgb.shape[1]
        print(f"Number of pixels in the image: {num_pixels}")

        io.imsave('captured_image.jpg', image_rgb)
        io.imsave('captured_image.png', image_rgb)

        print("Image saved as 'captured_image.jpg' and 'captured_image.png'.")


cap.release()
cv2.destroyAllWindows()

#OUTPUT
# Press 'Space' to capture an image and 'ESC' to exit.
# Number of pixels in the image: 307200
# Image saved as 'captured_image.jpg' and 'captured_image.png'.
