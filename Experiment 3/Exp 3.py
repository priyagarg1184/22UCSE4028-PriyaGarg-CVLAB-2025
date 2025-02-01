import cv2
import numpy as np
import tkinter as tk
from tkinter import Scale, HORIZONTAL

class WebcamAdjustmentsApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        # Open the default webcam
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: Could not open webcam.")
            exit()

        # Set up the sliders for adjustments
        self.create_sliders()
        
        self.update_frame()
        self.window.mainloop()

    def create_sliders(self):
        # Brightness slider
        self.brightness_slider = Scale(self.window, from_=0, to=255, orient=HORIZONTAL, label="Brightness")
        self.brightness_slider.set(128)
        self.brightness_slider.pack()

        # Contrast slider
        self.contrast_slider = Scale(self.window, from_=0, to=127, orient=HORIZONTAL, label="Contrast")
        self.contrast_slider.set(64)
        self.contrast_slider.pack()

        # Sharpness slider (simulated with kernel enhancement)
        self.sharpness_slider = Scale(self.window, from_=1, to=10, orient=HORIZONTAL, label="Sharpness")
        self.sharpness_slider.set(1)
        self.sharpness_slider.pack()

        # Hue slider (normalized as a shift in HSV hue values)
        self.hue_slider = Scale(self.window, from_=-90, to=90, orient=HORIZONTAL, label="Hue")
        self.hue_slider.set(0)
        self.hue_slider.pack()

        # Saturation slider
        self.saturation_slider = Scale(self.window, from_=-100, to=100, orient=HORIZONTAL, label="Saturation")
        self.saturation_slider.set(0)
        self.saturation_slider.pack()

    def apply_adjustments(self, frame):
        # Brightness and contrast adjustment
        brightness = self.brightness_slider.get() - 128
        contrast = self.contrast_slider.get()
        frame = cv2.convertScaleAbs(frame, alpha=1 + contrast / 127.0, beta=brightness)

        # Convert to HSV for hue and saturation adjustments
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype(np.float32)

        # Hue adjustment
        hue_shift = self.hue_slider.get()
        hsv_frame[:, :, 0] = (hsv_frame[:, :, 0] + hue_shift) % 180

        # Saturation adjustment
        saturation_shift = self.saturation_slider.get() / 100.0
        hsv_frame[:, :, 1] = np.clip(hsv_frame[:, :, 1] * (1 + saturation_shift), 0, 255)

        # Convert back to BGR
        frame = cv2.cvtColor(hsv_frame.astype(np.uint8), cv2.COLOR_HSV2BGR)

        # Sharpness adjustment using a kernel
        sharpness_level = self.sharpness_slider.get()
        if sharpness_level > 1:
            kernel = np.array([[-1, -1, -1], [-1, 9 + sharpness_level, -1], [-1, -1, -1]])
            frame = cv2.filter2D(frame, -1, kernel)

        return frame

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Failed to capture image")
            return

        # Apply adjustments to the frame
        frame = self.apply_adjustments(frame)

        # Display the image
        cv2.imshow("Webcam Adjustments", frame)

        # Schedule the next frame update
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.cap.release()
            cv2.destroyAllWindows()
            self.window.destroy()
        else:
            self.window.after(10, self.update_frame)

if __name__ == "__main__":
    root = tk.Tk()
    app = WebcamAdjustmentsApp(root, "Webcam Adjustments GUI")