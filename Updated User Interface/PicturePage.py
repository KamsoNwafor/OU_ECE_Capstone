import tkinter as tk
from Database import DatabaseManager as dbm
from PIL import ImageTk, Image
import io
import cv2
import os

# import the tk.Frame class that creates frames
class PictureFrame(tk.Frame):
    frame_index = 5

    # Initialize the Photo Capture Page
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master, bg="#fafafa")

        self.controller = controller
        self.cap = None  # Camera capture object
        self.preview_running = False  # Camera preview status
        self.photo_path = None  # Path to captured photo

        self.instruction = tk.Label(master = self)
        self.instruction.config(text = "Please touch the screen when you're ready to take the picture")
        self.instruction.grid(row = 1, column = 0, sticky="news")

        self.forward_button = tk.Button(master=self)  # button to go to the next page (report page)
        self.forward_button.config(width=20, text="Forward", command=lambda: self.complete_task())  # tries to update password, or tell user that password is wrong
        self.forward_button.grid(row=2, column=2, padx=10, pady=10,
                                 sticky="SE")  # places forward button at the bottom right of screen

        self.back_button = tk.Button(master=self)  # button to go to the previous page (battery selection page)
        self.back_button.config(width=20, text="Back", command=lambda: controller.back_button())
        self.back_button.grid(row=2, column=0, padx=10, pady=10, sticky="SW")  # places back button at the bottom left of screen

    def previous_page(self):
        # if find is selected, show find page
        if self.controller.selected_task_id == "1":
            self.controller.frames[5][1].find_item()
            self.controller.show_page(5)
        # if receive is selected, show receive page
        elif self.controller.selected_task_id == "2":
            self.controller.show_page(6)
        # if ship is selected, show ship page
        elif self.controller.selected_task_id == "3":
            self.controller.show_page(7)
        # if move is selected, show move page
        elif self.controller.selected_task_id == "4":
            self.controller.show_page(8)
        # if update battery status is selected, show update battery status page
        elif self.controller.selected_task_id == "5":
            self.controller.show_page(9)
        # if take picture is selected, show take picture page
        elif self.controller.selected_task_id == "21":
            self.controller.show_page(10)

    # Start the camera for live preview
    def start_camera(self):
        self.stop_camera()  # Ensure any existing camera is stopped
        try:
            self.cap = cv2.VideoCapture(0)  # Initialize camera
            if not self.cap.isOpened():
                tk.messagebox.showerror("Camera Error",
                                        "Failed to access camera. Please ensure the camera is connected and not in use.",
                                        parent=self.controller.root)
                self.cap = None
                return
        except Exception as e:
            tk.messagebox.showerror("Camera Error", f"Error initializing camera: {str(e)}",
                                    parent=self.controller.root)
            self.cap = None
            return

    def stop_camera(self):
        self.preview_running = False  # Stop preview updates
        if self.cap:
            try:
                self.cap.release()  # Release camera
            except Exception as e:
                print(f"Error releasing camera: {str(e)}")
            self.cap = None
        self.preview_label.configure(image="")  # Clear preview