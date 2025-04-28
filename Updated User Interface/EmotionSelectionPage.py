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

        # list to store emotions and adjectives
        self.emotions = ["Excited", "Tired", "Confident", "Frustrated", "Happy", "Bored"]
        self.adjectives = ["Challenging", "Rewarding", "Tiring", "Fun", "Stressful", "Interesting"]

        # store an instance of controller in frame, easier to manage controller data
        self.controller = controller

        # Create header with title
        header = tk.Frame(self, bg="#4CAF50")
        header.pack(fill="x")
        tk.Label(header, text="Step 6: Emotion Selection", font=("Roboto", 14, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(pady=15)

        # Create content frame
        content = tk.Frame(self, bg="#f0f0f0", bd=1, relief="solid")
        content.pack(pady=10, padx=10, fill="both", expand=True)
        content.grid_columnconfigure(0, weight=1)  # Center content

        # Mad Libs sentence label
        self.mad_libs_label = tk.Label(content, text="After working on this task, I feel [emotion] because it was a [adjective] experience!", 
                                       font=("Roboto", 12, "italic"), bg="#f0f0f0", fg="#333333", wraplength=400)
        self.mad_libs_label.grid(row=0, column=0, pady=(10, 15))

        # String Variable to store emotion options
        self.emotion_list = tk.StringVar(self)
        self.emotion_list.set("0")
        self.emotion_list.trace_add("write", self.update_mad_libs)

        # String Variable to store adjective options
        self.adjective_list = tk.StringVar(self)
        self.adjective_list.set("0")
        self.adjective_list.trace_add("write", self.update_mad_libs)

        # create instruction label for emotions
        self.emotion_label = tk.Label(content, text="Choose your emotion:", font=("Roboto", 12, "bold"), bg="#f0f0f0", fg="#212121")
        self.emotion_label.grid(row=1, column=0, pady=(5, 5))

        # emotion option tracker variable
        self.emotion_option = None

        # create instruction label for adjectives
        self.adjective_label = tk.Label(content, text="Choose an adjective:", font=("Roboto", 12, "bold"), bg="#f0f0f0", fg="#212121")
        self.adjective_label.grid(row=3, column=0, pady=(10, 5))

        # adjective option tracker variable
        self.adjective_option = None

        self.forward_button = None
        self.back_button = None

        # Initialize the radiobuttons
        self.update_emotion_list()

    def update_mad_libs(self, *args):
        # Get the selected emotion and adjective, default to placeholders if not selected
        emotion = self.emotion_list.get() if self.emotion_list.get() != "0" else "[emotion]"
        adjective = self.adjective_list.get() if self.adjective_list.get() != "0" else "[adjective]"
        # Update the Mad Libs sentence
        self.mad_libs_label.config(text=f"After working on this task, I feel {emotion} because it was a {adjective} experience!")

    def manage_option(self):
        # make sure that a button was actually clicked for both emotion and adjective
        if self.emotion_list.get() != "0" and self.adjective_list.get() != "0":
            # save the selected emotion and adjective
            self.controller.selected_emotion = self.emotion_list.get()
            self.controller.selected_adjective = self.adjective_list.get()

            # loads battery list and updates the user on the report selection page
            self.controller.frames[-1][1].load_report()
            self.controller.show_page(-1)

    def previous_page(self):
        self.rds_cursor.execute("SELECT * FROM batteries WHERE serial_number = %s", (self.controller.selected_battery_serial_number,))
        result = self.rds_cursor.fetchall()

        if not result:
            # go back to move page for intaking new batteries
            self.controller.show_page(8)
        else:
            # if find is selected, show find page
            if self.controller.selected_task_id == "1":
                self.controller.show_page(5)
            # if not, then show take picture page, since every other instruction needs a picture
            else:
                self.controller.show_page(8)

    def update_emotion_list(self):
        # track number of emotions
        content = self.emotion_label.master  # Get the content frame (parent of emotion_label)
        index = 2  # Start after emotion_label (row 1)
        for emotion in self.emotions:
            # creates a single-selection list for each emotion
            self.emotion_option = ttk.Radiobutton(content, text=emotion, variable=self.emotion_list, value=emotion)
            # place the choices in the centre, one after the other
            self.emotion_option.grid(row=index, column=0, padx=10, pady=5, sticky="w")
            index += 1

        # Update adjective label row
        self.adjective_label.grid(row=index, column=0, pady=(10, 5))
        index += 1

        # Add adjective radiobuttons
        for adjective in self.adjectives:
            self.adjective_option = ttk.Radiobutton(content, text=adjective, variable=self.adjective_list, value=adjective)
            self.adjective_option.grid(row=index, column=0, padx=10, pady=5, sticky="w")
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
