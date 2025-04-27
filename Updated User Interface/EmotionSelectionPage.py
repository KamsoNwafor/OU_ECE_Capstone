

import tkinter as tk
from tkinter import ttk
from Database import DatabaseManager as dbm

# import the tk.Frame class that creates frames
class EmotionSelectionFrame(tk.Frame):
    # store relative frame index number
    frame_index = 12

    def __init__(self, master, controller):
        # initialise the imported class
        tk.Frame.__init__(self, master, bg="#fafafa")  # Set soft background color

        # connect to database and create cursor to traverse through database
        self.rds_conn = dbm.get_rds_conn()
        self.rds_cursor = self.rds_conn.cursor()

        # list to store emotions
        self.emotions = ["Excited", "Tired", "Confident", "Frustrated", "Happy", "Bored"]

        # store an instance of controller in frame, easier to manage controller data
        self.controller = controller

        # Create header with title
        header = tk.Frame(self, bg="#4CAF50")
        header.pack(fill="x")
        tk.Label(header, text="Step 6: Emotion Selection", font=("Roboto", 14, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(pady=15)

        # Create content frame
        content = tk.Frame(self, bg="#f0f0f0", bd=1, relief="solid")
        content.pack(pady=10, padx=10, fill="both", expand=True)

        # create instruction label and place instruction label in top-centre area of frame
        self.emotion_label = tk.Label(content, text="How are you feeling?", font=("Roboto", 12, "bold"), bg="#f0f0f0", fg="#212121")
        self.emotion_label.grid(row=0, column=0, pady=(10, 5))

        # String Variable to store button options
        # Initial value must be different from options listed in order to avoid selection errors
        self.emotion_list = tk.StringVar(self)
        self.emotion_list.set("0")

        # emotion option tracker variable.
        # Don't initialise positions of buttons, as they depend on the tracker variable
        self.emotion_option = None
        self.forward_button = None
        self.back_button = None

    def manage_option(self):
        # make sure that a button was actually clicked
        if self.emotion_list.get() != "0":
            # save the selected emotion's value
            self.controller.selected_emotion = self.emotion_list.get()

            # loads battery list and updates the user on the battery selection page
            self.controller.frames[-1][1].load_report()
            self.controller.show_page(-1)

    def previous_page(self):
        # if find is selected, show find page
        if self.controller.selected_task_id == "1":
            self.controller.show_page(5)
        # if not, then show take picture page, since every other instruction needs a picture
        else:
            self.controller.show_page(8)

    def update_emotion_list(self):
        # track number of emotions
        content = self.emotion_label.master  # Get the content frame (parent of emotion_label)
        index = 1
        for emotion in self.emotions:
            # creates a single-selection list for each emotion
            self.emotion_option = ttk.Radiobutton(content, text=emotion, variable=self.emotion_list, value=emotion)

            # place the choices in the centre, one after the other
            self.emotion_option.grid(row=index, column=0, padx=10, pady=5, sticky="w")
            index += 1

        # Navigation buttons
        nav_frame = tk.Frame(content, bg="#f0f0f0")
        nav_frame.grid(row=index, column=0, pady=10)

        # button to go to the previous logical page (dependent on)
        self.back_button = ttk.Button(nav_frame, text="Back", style="Secondary.TButton", command=self.previous_page)
        self.back_button.pack(side="left", padx=5)

        # button to go to the next page (report page)
        # the button saves the emotion selected and goes to the next page (report page) when clicked
        self.forward_button = ttk.Button(nav_frame, text="Forward", style="Primary.TButton", command=self.manage_option)
        self.forward_button.pack(side="left", padx=5)
