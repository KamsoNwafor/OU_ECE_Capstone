import tkinter as tk
from tkinter import ttk
from Database import DatabaseManager as dbm

# import the tk.Frame class that creates frames
class BatteryStateFrame(tk.Frame):
    # store relative frame index number
    frame_index = 10

    def __init__(self, master, controller):
        # initialise the imported class
        tk.Frame.__init__(self, master, bg="#fafafa")  # Set soft background color

        # connect to database and create cursor to traverse through database
        self.rds_conn = dbm.get_rds_conn()
        self.rds_cursor = self.rds_conn.cursor()

        # empty variable to store state names
        self.states = None

        # store an instance of controller in frame, easier to manage controller data
        self.controller = controller

        # Create header with title
        header = tk.Frame(self, bg="#4CAF50")
        header.pack(fill="x")
        tk.Label(header, text="Step 6: Battery State", font=("Roboto", 14, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(pady=15)

        # Create content frame
        content = tk.Frame(self, bg="#f0f0f0", bd=1, relief="solid")
        content.pack(pady=10, padx=10, fill="both", expand=True)

        # create instruction label and place instruction label in top-centre area of frame
        self.state_label = tk.Label(content, text="What is the battery state?", font=("Roboto", 12, "bold"), bg="#f0f0f0", fg="#212121")
        self.state_label.grid(row=0, column=0, pady=(10, 5))

        # String Variable to store button options
        # Initial value must be different from options listed in order to avoid selection errors
        self.state_list = tk.StringVar(self)
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
        self.rds_cursor.execute("SELECT * FROM battery_state")

        # loads the main states into the state selection list
        self.states = self.rds_cursor.fetchall()

        # Add radiobuttons to the content frame
        content = self.state_label.master  # Get the content frame (parent of state_label)
        index = 1
        for state in self.states:
            # creates a single-selection list for each state
            self.state_option = ttk.Radiobutton(content, text=state[1], variable=self.state_list, value=state[0])

            # place the choices in the centre, one after the other
            self.state_option.grid(row=index, column=0, padx=10, pady=5, sticky="w")
            index += 1

        # Navigation buttons
        nav_frame = tk.Frame(content, bg="#f0f0f0")
        nav_frame.grid(row=index, column=0, pady=10)

        # button to go to the previous logical page (receive page)
        self.back_button = ttk.Button(nav_frame, text="Back", style="Secondary.TButton", command=self.previous_page)
        self.back_button.pack(side="left", padx=5)

        # button to go to the next page (item selection page)
        # the button saves the state id selected and goes to the next page when clicked
        self.forward_button = ttk.Button(nav_frame, text="Forward", style="Primary.TButton", command=self.manage_option)
        self.forward_button.pack(side="left", padx=5)

    def previous_page(self):
        self.controller.show_page(6)
        self.controller.selected_state_id = None


