import tkinter as tk
from Database import DatabaseManager as dbm

# import the tk.Frame class that creates frames
class BatteryStateFrame(tk.Frame):
    # store relative frame index number
    frame_index = 10

    def __init__(self, master, controller):
        # initialise the imported class
        tk.Frame.__init__(self, master)

        # connect to database and create cursor to traverse through database
        self.rds_conn = dbm.get_rds_conn()
        self.rds_cursor = self.rds_conn.cursor()

        # empty variable to store state names
        self.states = None

        # store an instance of controller in frame, easier to manage controller data
        self.controller = controller

        # create instruction label and place instruction label in top-centre area of frame
        self.state_label = tk.Label(master = self)
        self.state_label.config(text = "What is the battery state?")
        self.state_label.grid(row = 0, column  = 1)

        # String Variable to store button options
        # Initial value must be different from options listed in order to avoid selection errors
        self.state_list = tk.StringVar(master = self)
        self.state_list.set("0")

        # state option tracker variable.
        # Don't initialise positions of buttons, as they depend on the tracker variable
        self.state_option = None
        self.forward_button = None
        self.back_button = None

    def manage_option(self):
        # make sure that a button was actually clicked
        if self.state_list.get() != "0":
            # save the selected state's value
            self.controller.selected_state_id = self.state_list.get()

            # load battery state action page
            self.controller.frames[11][1].load_actions()
            self.controller.show_page(11)


    def update_state_list(self):
        # searches for the main states wanted listed by spiers in the database
        self.rds_cursor.execute("""
        select *
        from battery_state;
        """)

        # loads the main states into the state selection list
        self.states = self.rds_cursor.fetchall()

        index = 1
        for state in self.states:
            # creates a single-selection list for each state
            self.state_option = tk.Radiobutton(master=self)

            # labels each choice by the relevant state and gives it a place value
            self.state_option.config(text=state[1], variable=self.state_list, value=state[0])

            # place the choices in the centre, one after the other
            self.state_option.grid(row=index, column=1, padx=10, pady=10, sticky="NEWS")
            index += 1

        # button to go to the next page (item selection page)
        # the button saves the state id selected and goes to the next page when clicked
        self.forward_button = tk.Button(master=self)
        self.forward_button.config(width=20, text="Forward", command=lambda: self.manage_option())

        # place the forward button at the bottom right of screen
        self.forward_button.grid(row=index, column=2, padx=10, pady=10, sticky="SE")

        # button to go to the previous logical page (receive page)
        self.back_button = tk.Button(master=self)
        self.back_button.config(width=20, text="Back", command=lambda: self.previous_page())

        # places back button at the bottom left of screen
        self.back_button.grid(row=index, column=0, padx=10, pady=10, sticky="SW")

    def previous_page(self):

        self.controller.show_page(6)
        self.controller.selected_state_id = None

