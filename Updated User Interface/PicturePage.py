import math
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import cv2
from Database import DatabaseManager as dbm
import tkinter.messagebox as messagebox  # For popup

class PictureFrame(tk.Frame):
    frame_index = 8

    def __init__(self, master, controller):
        # Initialize frame with soft background
        tk.Frame.__init__(self, master, bg="#fafafa")
        self.controller = controller

        # Connect to RDS database
        self.rds_conn = dbm.get_rds_conn()
        self.rds_cursor = self.rds_conn.cursor()

        # Camera and image variables
        self.cam = None
        self.ret = None
        self.frame = None
        self.frame_rgb = None
        self.filename = "captured_photo.jpg"

        self.capture = False  # Flag to trigger capture
        self.image = None
        self.image_tk = None
        self.max_width = math.floor(800 / 3)
        self.max_height = math.floor(480 / 3)

        # Header
        header = tk.Frame(self, bg="#4CAF50")
        header.pack(fill="x")
        tk.Label(header, text="Step 5: Take Picture", font=("Roboto", 14, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(pady=10)

        # Main content
        content = tk.Frame(self, bg="#f0f0f0", bd=1, relief="solid")
        content.pack(padx=5, pady=5, fill="both", expand=True)

        # Instruction label
        self.instruction = tk.Label(content, text="Please touch the screen when you're ready to take the picture",
                                    font=("Roboto", 12, "bold"), bg="#f0f0f0", fg="#212121")
        self.instruction.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="news")

        # Image preview label
        self.image_label = tk.Label(content, bg="#f0f0f0")
        self.image_label.grid(row=1, column=0, padx=10, pady=10, sticky="news")
        self.image_label.bind("<Button-1>", self.capture_on_click)

        # Navigation buttons
        nav_frame = tk.Frame(content, bg="#f0f0f0")
        nav_frame.grid(row=2, column=0, pady=10)

        self.back_button = ttk.Button(nav_frame, text="Back", style="Secondary.TButton", command=self.previous_page)
        self.back_button.pack(side="left", padx=5)

        self.retake_button = ttk.Button(nav_frame, text="Retake", style="Secondary.TButton", command=self.image_preview)
        self.retake_button.pack(side="left", padx=5)

        self.forward_button = ttk.Button(nav_frame, text="Forward", style="Primary.TButton", command=self.next_page)
        self.forward_button.pack(side="left", padx=5)

    def image_preview(self):
        # Start camera preview or handle missing camera
        self.capture = False
        if not self.open_camera():
            print("Camera not available. Proceeding without picture.")

            # Show friendly popup
            messagebox.showinfo("Camera Not Available", "Camera is not available.\nProceeding without a picture...")

            # After 2 seconds, proceed automatically
            self.after(2000, self.next_page)
        else:
            self.show_preview()

    def open_camera(self):
        # Attempt to open the default camera
        cam_port = 0
        self.cam = cv2.VideoCapture(cam_port)

        if not self.cam.isOpened():
            return False  # Camera not available
        else:
            # Configure camera resolution
            self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, self.max_width)
            self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, self.max_height)
            return True

    def show_preview(self):
        # Display live camera feed
        if self.cam and self.cam.isOpened():
            self.ret, self.frame = self.cam.read()
            if self.ret:
                self.frame = cv2.resize(self.frame, (self.max_width * 2, self.max_height * 2))
                self.frame_rgb = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                self.image = Image.fromarray(self.frame_rgb)
                self.image_tk = ImageTk.PhotoImage(image=self.image)
                self.image_label.configure(image=self.image_tk)

                if not self.capture:
                    self.after(10, self.show_preview)
                else:
                    self.save_image()
                    self.cam.release()

    def capture_on_click(self, event):
        # Trigger capture when screen is touched
        self.capture = True

    def save_image(self):
        # Save captured frame to file
        if self.frame is not None:
            cv2.imwrite(self.filename, self.frame)
            print(f"Image saved as {self.filename}")
            self.controller.selected_picture = Image.open(self.filename)

    def previous_page(self):
        # Navigate to appropriate previous page
        if self.cam and self.cam.isOpened():
            self.cam.release()

        self.rds_cursor.execute("SELECT * FROM batteries WHERE serial_number = ?", (self.controller.selected_battery_serial_number,))
        result = self.rds_cursor.fetchall()

        if not result:
            self.controller.show_page(7)
        else:
            if self.controller.selected_task_id == "2":
                self.controller.show_page(11)
                self.controller.selected_actions = None
            elif self.controller.selected_task_id == "3":
                self.controller.show_page(6)
                self.controller.selected_client_id = None
            elif self.controller.selected_task_id == "4":
                self.controller.show_page(7)
                self.controller.selected_location_id = None
            elif self.controller.selected_task_id == "20":
                self.controller.show_page(4)
                self.controller.selected_battery_serial_number = None

    def next_page(self):
        # Move to the emotion selection page
        if self.cam and self.cam.isOpened():
            self.cam.release()
        self.controller.frames[-2][1].update_emotion_list()
        self.controller.show_page(-2)
