import math
import tkinter as tk
from Database import DatabaseManager as dbm
from PIL import ImageTk, Image
import io
import cv2
import os

# import the tk.Frame class that creates frames
class PictureFrame(tk.Frame):
    frame_index = 7 # will be 10 on the final UI

    # Initialize the Photo Capture Page
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master, bg="#fafafa")

        self.controller = controller
        self.cam = None
        self.ret = None
        self.frame = None
        self.frame_rgb = None

        # Flag to indicate when to capture the image
        self.capture = False

        self.image = None
        self.max_width = math.floor(800 / 3)
        self.max_height = math.floor(480 / 3)
        self.image_tk = None
        self.image_label = tk.Label(master=self)
        self.image_label.grid(row=1, column=0, rowspan=2, columnspan=3, padx=10, pady=10, sticky="news")

        self.image_label.bind("<Button-1>", self.capture_on_click)

        self.instruction = tk.Label(master = self)
        self.instruction.config(text = "Please touch the screen when you're ready to take the picture")
        self.instruction.grid(row = 0, column = 1, padx = 10, pady = 10, sticky="news")

        # creates button to go to the next page (report page) and places it at the bottom right of screen
        self.forward_button = tk.Button(master=self)
        self.forward_button.config(width=20, text="Forward", command=lambda: self.next_page())
        self.forward_button.grid(row=3, column=2, padx=10, pady=10, sticky="SE")

        # creates button to go retake picture
        self.retake_button = tk.Button(master=self)
        self.retake_button.config(width=20, text="Retake", command=lambda: self.image_preview())
        self.retake_button.grid(row=3, column=1, padx=10, pady=10, sticky="S")

        self.back_button = tk.Button(master=self)  # button to go to the previous page (battery selection page)
        self.back_button.config(width=20, text="Back", command=lambda: self.previous_page())
        self.back_button.grid(row=3, column=0, padx=10, pady=10, sticky="WE")  # places back button at the bottom left of screen

    def image_preview(self):
        self.capture = False
        self.open_camera()
        self.show_preview()

    def show_preview(self):
        if self.cam.isOpened():
            # reading the input using the camera
            self.ret, self.frame = self.cam.read()

            if self.ret:
                self.frame = cv2.resize(self.frame, (self.max_width * 2, self.max_height * 2))  # Resize frame
                self.frame_rgb = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
                self.image = Image.fromarray(self.frame_rgb)
                self.image_tk = ImageTk.PhotoImage(image=self.image)
                self.image_label.configure(image=self.image_tk)

                if not self.capture:
                    self.after(10, self.show_preview)
                else:
                    self.save_image()
                    self.cam.release()

    def open_camera(self):
        cam_port = 0
        self.cam = cv2.VideoCapture(cam_port)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, self.max_width)  # Set width
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, self.max_height)  # Set height

    def capture_on_click(self, event):
        self.capture = True

    def save_image(self):
        if self.frame is not None:
            filename = "captured_photo.jpg"
            cv2.imwrite(filename, cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR))  # Save the frame as an image
            print(f"Image saved as {filename}")
            self.controller.selected_picture = Image.open(filename)


    def previous_page(self):
        # if receive or ship is selected, show battery status action page
        if (self.controller.selected_task_id == "2"
        or self.controller.selected_task_id == "3"):
            self.controller.show_page(11)
            self.controller.selected_actions = None
        # if move is selected, show move page
        elif self.controller.selected_task_id == "4":
            self.controller.show_page(7)
        # if take picture is selected, go to item selection page
        elif self.controller.selected_task_id == "20":
            self.controller.show_page(4)
        # if intake new item is selected, go to new item page
        elif self.controller.selected_task_id == "21":
            self.controller.show_page(9)

        self.controller.selected_picture = None

    def next_page(self):
        self.controller.frames[-2][1].update_emotion_list()
        self.controller.forward_button()

