import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import cv2
import time
import os

class PhotoPage(tk.Frame):
    # Initialize the Photo Capture Page
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#fafafa")
        self.controller = controller
        self.cap = None  # Camera capture object
        self.preview_running = False  # Camera preview status
        self.photo_path = None  # Path to captured photo

        # Create header with title
        header = tk.Frame(self, bg="#4CAF50")
        header.pack(fill="x")
        tk.Label(header, text="Step 6: Take Photo", font=("Roboto", 14, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(pady=15)

        # Create content frame
        content = tk.Frame(self, bg="#f0f0f0", bd=1, relief="solid")
        content.pack(pady=10, padx=10, fill="both", expand=True)
        tk.Label(content, text="Capture item photo:", font=("Roboto", 12, "bold"), bg="#f0f0f0", fg="#212121").pack(pady=10)

        # Camera preview label
        self.preview_label = tk.Label(content, bg="#f0f0f0")
        self.preview_label.pack(pady=10)

        # Capture and retake buttons
        btn_frame = tk.Frame(content, bg="#f0f0f0")
        btn_frame.pack(pady=10)
        self.capture_btn = ttk.Button(btn_frame, text="Capture", style="Primary.TButton", command=self.capture_photo)
        self.capture_btn.pack(side="left", padx=5)
        self.retake_btn = ttk.Button(btn_frame, text="Retake", style="Secondary.TButton", command=self.retake_photo, state="disabled")
        self.retake_btn.pack(side="left", padx=5)

        # Navigation buttons
        nav_frame = tk.Frame(content, bg="#f0f0f0")
        nav_frame.pack(pady=10)
        back_btn = ttk.Button(nav_frame, text="Back", style="Secondary.TButton", command=lambda: self.controller.go_back("PhotoPage"))
        back_btn.pack(side="left", padx=5)
        next_btn = ttk.Button(nav_frame, text="Next", style="Primary.TButton", command=lambda: self.controller.validate_and_proceed("PhotoPage", "ReactionPage", self.controller.photo_taken.get(), "Photo capture"))
        next_btn.pack(side="left", padx=5)

    # Start the camera for live preview
    def start_camera(self):
        self.stop_camera()  # Ensure any existing camera is stopped
        try:
            self.cap = cv2.VideoCapture(0)  # Initialize camera
            if not self.cap.isOpened():
                messagebox.showerror("Camera Error", "Failed to access camera. Please ensure the camera is connected and not in use.", parent=self.controller.root)
                self.cap = None
                return
        except Exception as e:
            messagebox.showerror("Camera Error", f"Error initializing camera: {str(e)}", parent=self.controller.root)
            self.cap = None
            return

        self.preview_running = True  # Enable preview
        self.update_preview()  # Start updating preview

    # Update camera preview frame
    def update_preview(self):
        if not self.preview_running or not self.cap:
            return

        try:
            ret, frame = self.cap.read()  # Read camera frame
            if ret:
                frame = cv2.resize(frame, (320, 240))  # Resize frame
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
                img = Image.fromarray(frame_rgb)
                imgtk = ImageTk.PhotoImage(image=img)
                self.preview_label.imgtk = imgtk  # Keep reference
                self.preview_label.configure(image=imgtk)
            else:
                messagebox.showwarning("Camera Warning", "Failed to read frame from camera.", parent=self.controller.root)
                self.stop_camera()
                return
        except Exception as e:
            messagebox.showerror("Preview Error", f"Error updating preview: {str(e)}", parent=self.controller.root)
            self.stop_camera()
            return

        self.after(10, self.update_preview)  # Schedule next update

    # Capture a photo from the camera
    def capture_photo(self):
        if not self.cap or not self.cap.isOpened():
            messagebox.showerror("Camera Error", "Camera is not available. Please restart the application.", parent=self.controller.root)
            return

        try:
            ret, frame = self.cap.read()  # Read frame
            if ret:
                timestamp = time.strftime("%Y%m%d_%H%M%S")  # Generate timestamp
                self.photo_path = f"photo_{timestamp}.jpg"  # Set photo filename
                if not os.access(".", os.W_OK):
                    messagebox.showerror("Storage Error", "No write permission in the current directory.", parent=self.controller.root)
                    return
                cv2.imwrite(self.photo_path, frame)  # Save photo
                self.controller.photo_taken.set(True)  # Mark photo as taken
                self.capture_btn.configure(state="disabled")  # Disable capture button
                self.retake_btn.configure(state="normal")  # Enable retake button
                messagebox.showinfo("Photo Captured", f"Photo saved as {self.photo_path}", parent=self.controller.root)
            else:
                messagebox.showerror("Capture Error", "Failed to capture photo.", parent=self.controller.root)
        except Exception as e:
            messagebox.showerror("Capture Error", f"Error saving photo: {str(e)}", parent=self.controller.root)

    # Retake a photo by deleting the previous one
    def retake_photo(self):
        if self.photo_path and os.path.exists(self.photo_path):
            try:
                os.remove(self.photo_path)  # Delete existing photo
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete photo: {str(e)}", parent=self.controller.root)
        self.controller.photo_taken.set(False)  # Reset photo taken flag
        self.capture_btn.configure(state="normal")  # Enable capture button
        self.retake_btn.configure(state="disabled")  # Disable retake button
        self.start_camera()  # Restart camera

    # Stop the camera and clear preview
    def stop_camera(self):
        self.preview_running = False  # Stop preview updates
        if self.cap:
            try:
                self.cap.release()  # Release camera
            except Exception as e:
                print(f"Error releasing camera: {str(e)}")
            self.cap = None
        self.preview_label.configure(image="")  # Clear preview
