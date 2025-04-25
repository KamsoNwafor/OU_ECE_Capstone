import tkinter as tk
from Database import DatabaseManager as dbm

# import the tk.Frame class that creates frames
class EmotionSelectionFrame(tk.Frame):
    # store relative frame index number
    frame_index = 3

    def __init__(self, master, controller):
        # initialise the imported class
        tk.Frame.__init__(self, master)

        # connect to database and create cursor to traverse through database
        self.rds_conn = dbm.get_rds_conn()
        self.rds_cursor = self.rds_conn.cursor()

        # list to store emotions
        self.emotions = ["Excited", "Tired", "Confident", "Frustrated", "Happy", "Bored"]

        # store an instance of controller in frame, easier to manage controller data
        self.controller = controller

        # create instruction label and place instruction label in top-centre area of frame
        self.emotion_label = tk.Label(master = self)
        self.emotion_label.config(text = "How are you feeling")
        self.emotion_label.grid(row = 0, column  = 1)

        # String Variable to store button options
        # Initial value must be different from options listed in order to avoid selection errors
        self.emotion_list = tk.StringVar(master = self)
        self.emotion_list.set("0")

        # emotion option tracker variable.
        # Don't initialise positions of buttons, as they depend on the tracker variable
        self.emotion_option = None
        self.forward_button = None
        self.back_button = None

    def manage_option(self):
        # save the selected emotion's value
        self.controller.selected_emotion = self.emotion_list.get()

        # loads battery list and updates the user on the battery selection page
        self.controller.frames[-1][1].load_report()
        self.controller.forward_button()

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

    def update_emotion_list(self):
        # track number of emotions
        index = 1
        for emotion in self.emotions:
            # creates a single-selection list for each emotion
            self.emotion_option = tk.Radiobutton(master=self)

            # labels each choice by the relevant emotion and gives it a place value
            self.emotion_option.config(text=emotion, variable=self.emotion_list, value=emotion)

            # place the choices in the centre, one after the other
            self.emotion_option.grid(row=index, column=1, padx=10, pady=10, sticky="NEWS")
            index += 1

        # button to go to the next page (report page)
        # the button saves the emotion selected and goes to the next page (report page) when clicked
        self.forward_button = tk.Button(master=self)
        self.forward_button.config(width=20, text="Forward", command=lambda: self.manage_option())

        # place the forward button at the bottom right of screen
        self.forward_button.grid(row=index, column=2, padx=10, pady=10, sticky="SE")

        # button to go to the previous logical page (dependent on)
        self.back_button = tk.Button(master=self)
        self.back_button.config(width=20, text="Back", command=lambda: self.previous_page())

        # places back button at the bottom left of screen
        self.back_button.grid(row=index, column=0, padx=10, pady=10, sticky="SW")

