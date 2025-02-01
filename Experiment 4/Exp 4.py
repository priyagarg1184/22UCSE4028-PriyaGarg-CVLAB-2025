import cv2
import numpy as np
import matplotlib.pyplot as plt

def high_pass_filter(img_fft, threshold=30):
    rows, cols = img_fft.shape
    crow, ccol = rows // 2, cols // 2

    # Create a mask with a high-pass region
    mask = np.ones((rows, cols), np.uint8)
    mask[crow - threshold:crow + threshold, ccol - threshold:ccol + threshold] = 0

    # Apply the mask to the FFT image
    filtered_fft = img_fft * mask
    return filtered_fft


def low_pass_filter(img_fft, threshold=30):
    rows, cols = img_fft.shape
    crow, ccol = rows // 2, cols // 2

    # Create a mask with a low-pass region
    mask = np.zeros((rows, cols), np.uint8)
    mask[crow - threshold:crow + threshold, ccol - threshold:ccol + threshold] = 1

    # Apply the mask to the FFT image
    filtered_fft = img_fft * mask
    return filtered_fft


def apply_fourier_filter(image_path, output_high_pass, output_low_pass):
    # Read the image in grayscale
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print("Error: Image not found.")
        return

    # Perform FFT and shift the zero frequency component to the center
    dft = np.fft.fft2(img)
    dft_shift = np.fft.fftshift(dft)

    # Apply High Pass Filter
    high_pass_fft = high_pass_filter(dft_shift)
    high_pass_img = np.abs(np.fft.ifft2(np.fft.ifftshift(high_pass_fft)))

    # Apply Low Pass Filter
    low_pass_fft = low_pass_filter(dft_shift)
    low_pass_img = np.abs(np.fft.ifft2(np.fft.ifftshift(low_pass_fft)))

    # Normalize and save the filtered images
    high_pass_img = cv2.normalize(high_pass_img, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    low_pass_img = cv2.normalize(low_pass_img, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    cv2.imwrite(output_high_pass, high_pass_img)
    cv2.imwrite(output_low_pass, low_pass_img)

    # Show the results for visualization
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 3, 1)
    plt.title("Original Image")
    plt.imshow(img, cmap='gray')
    plt.axis('off')

    plt.subplot(1, 3, 2)
    plt.title("High Pass Filtered")
    plt.imshow(high_pass_img, cmap='gray')
    plt.axis('off')

    plt.subplot(1, 3, 3)
    plt.title("Low Pass Filtered")
    plt.imshow(low_pass_img, cmap='gray')
    plt.axis('off')

    plt.show()


if __name__ == "__main__":
    image_path = "C:\\Users\DELL\\OneDrive\Desktop\\Computer Vision Lab Work\\Experiment 4\\Original Image.jpg" 
    output_high_pass = "high_pass_filtered.jpg"
    output_low_pass = "low_pass_filtered.jpg"

    apply_fourier_filter(image_path, output_high_pass, output_low_pass)
