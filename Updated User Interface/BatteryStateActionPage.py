import tkinter as tk
from tkinter import ttk
from Database import DatabaseManager as dbm

# import the tk.Frame class that creates frames
class BatteryStateActionFrame(tk.Frame):
    # store relative frame index number
    frame_index = 11

    new_battery = 6
    old_battery = 7
    death_row_battery = 8

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master, bg="#fafafa")  # Set soft background color

        self.controller = controller

        self.actions = None

        self.rds_conn = dbm.get_rds_conn()  # connect to local database
        self.rds_cursor = self.rds_conn.cursor()  # create cursor to search through local database

        self.action_check = None
        self.forward_button = None
        self.back_button = None

        self.battery_action = None

        self.action_vars = []
        self.selected_actions = []
        self.checks = []

        # Create header with title
        header = tk.Frame(self, bg="#4CAF50")
        header.pack(fill="x")
        tk.Label(header, text="Step 7: Battery Actions", font=("Roboto", 14, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(pady=15)

        # Create content frame
        content = tk.Frame(self, bg="#f0f0f0", bd=1, relief="solid")
        content.pack(pady=10, padx=10, fill="both", expand=True)

        # create instruction label
        self.action_prompt = tk.Label(content, text="Please Select the Actions You Have Completed", font=("Roboto", 12, "bold"), bg="#f0f0f0", fg="#212121")
        self.action_prompt.grid(row=0, column=0, pady=(10, 5))

    def finalise_list(self):
        # make sure the user clicked that they did something
        if self.selected_actions:
            self.controller.selected_actions = self.selected_actions
            self.controller.frames[8][1].image_preview()
            self.controller.show_page(8)

    def load_actions(self):
        if self.controller.selected_state_id == "1":
            self.battery_action = self.new_battery
        elif self.controller.selected_state_id == "2":
            self.battery_action = self.old_battery
        elif self.controller.selected_state_id == "3":
            self.battery_action = self.death_row_battery

        self.rds_cursor.execute("""
            SELECT work_type_id, work_type_name
            FROM works
            WHERE parent_work_type_id = %s
            OR work_type_id = 5
            ORDER BY work_type_id
        """, (self.battery_action,))  # work_type_id = 5 is the monitor battery status command

        self.actions = self.rds_cursor.fetchall()

        # Add checkbuttons to the content frame
        content = self.action_prompt.master  # Get the content frame (parent of action_prompt)
        index = 1
        for action in self.actions:
            action_var = tk.IntVar()
            self.action_check = ttk.Checkbutton(content, text=action[1], onvalue=action[0], offvalue=0, variable=action_var, command=self.update_actions_list)
            self.action_check.grid(row=index, column=0, padx=10, pady=5, sticky="w")
            self.action_vars.append(action_var)
            self.checks.append(self.action_check)
            index += 1

        # Navigation buttons
        nav_frame = tk.Frame(content, bg="#f0f0f0")
        nav_frame.grid(row=index, column=0, pady=10)

        # button to go to the previous page (battery state page), places back button at the bottom left of screen
        self.back_button = ttk.Button(nav_frame, text="Back", style="Secondary.TButton", command=self.previous_page)
        self.back_button.pack(side="left", padx=5)

        # creates button to go to the next page (selected task), places forward button at the bottom right of screen
        # if a list item is highlighted, then the forward button is clicked, select it
        self.forward_button = ttk.Button(nav_frame, text="Forward", style="Primary.TButton", command=self.finalise_list)
        self.forward_button.pack(side="left", padx=5)

    def update_actions_list(self):
        self.selected_actions.clear()

        for action_var in self.action_vars:
            if action_var.get() != 0:
                self.selected_actions.append(action_var.get())

    def previous_page(self):
        self.controller.show_page(10)

        index = 0
        for action_var in self.action_vars:
            if action_var.get() != 0:
                action_var.set(0)
            index += 1

        for button in self.checks:
            button.destroy()

        self.forward_button.destroy()
        self.back_button.destroy()

        self.selected_actions.clear()
        self.controller.selected_state_id = None
