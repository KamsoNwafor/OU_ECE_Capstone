import tkinter as tk
from tkinter import ttk
from Database import DatabaseManager as dbm

class BatteryStateActionFrame(tk.Frame):
    frame_index = 11

    new_battery = 6
    old_battery = 7
    death_row_battery = 8

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master, bg="#fafafa")  # Set soft background color
        self.controller = controller

        # Connect to RDS database
        self.rds_conn = dbm.get_rds_conn()
        self.rds_cursor = self.rds_conn.cursor()

        # Initialize variables
        self.actions = None
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
        tk.Label(header, text="Step 7: Battery Actions", font=("Roboto", 14, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(pady=10)

        # Create content frame
        content = tk.Frame(self, bg="#f0f0f0", bd=1, relief="solid")
        content.pack(pady=5, padx=5, fill="x", expand=False)
        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=1)

        # Instruction label
        self.action_prompt = tk.Label(content, text="Please Select the Actions You Have Completed", font=("Roboto", 12, "bold"), bg="#f0f0f0", fg="#212121")
        self.action_prompt.grid(row=0, column=0, columnspan=2, pady=(10, 10))

    def finalise_list(self):
        # Save selected actions and move to the next page
        if self.selected_actions:
            self.controller.selected_actions = self.selected_actions
            self.controller.frames[8][1].image_preview()
            self.controller.show_page(8)

    def load_actions(self):
        # Decide which set of actions to load based on battery state
        if self.controller.selected_state_id == "1":
            self.battery_action = self.new_battery
        elif self.controller.selected_state_id == "2":
            self.battery_action = self.old_battery
        elif self.controller.selected_state_id == "3":
            self.battery_action = self.death_row_battery

        # Fetch the actions from the database
        self.rds_cursor.execute("""
            SELECT work_type_id, work_type_name
            FROM works
            WHERE parent_work_type_id = %s
            OR work_type_id = 5
            ORDER BY work_type_id
        """, (self.battery_action,))

        self.actions = self.rds_cursor.fetchall()

        # Display actions as checkbuttons in two columns
        content = self.action_prompt.master
        split_point = (len(self.actions) + 1) // 2  # Halfway point

        for index, action in enumerate(self.actions):
            action_var = tk.IntVar()
            if index < split_point:
                row = index + 1
                column = 0
            else:
                row = index - split_point + 1
                column = 1

            self.action_check = ttk.Checkbutton(content, text=action[1], onvalue=action[0], offvalue=0, variable=action_var, command=self.update_actions_list)
            self.action_check.grid(row=row, column=column, padx=10, pady=3, sticky="w")

            self.action_vars.append(action_var)
            self.checks.append(self.action_check)

        # Navigation buttons (Back and Forward)
        nav_frame = tk.Frame(content, bg="#f0f0f0")
        nav_frame.grid(row=max(split_point, len(self.actions) - split_point) + 2, column=0, columnspan=2, pady=(10, 2))

        nav_frame.grid_columnconfigure(0, weight=1)
        nav_frame.grid_columnconfigure(1, weight=1)

        self.back_button = ttk.Button(nav_frame, text="Back", style="Secondary.TButton", command=self.previous_page)
        self.back_button.grid(row=0, column=0, padx=5)

        self.forward_button = ttk.Button(nav_frame, text="Forward", style="Primary.TButton", command=self.finalise_list)
        self.forward_button.grid(row=0, column=1, padx=5)

    def update_actions_list(self):
        # Update the list of selected action IDs
        self.selected_actions.clear()
        for action_var in self.action_vars:
            if action_var.get() != 0:
                self.selected_actions.append(action_var.get())

    def previous_page(self):
        # Reset selections and return to previous page
        self.controller.show_page(10)

        for action_var in self.action_vars:
            action_var.set(0)

        for button in self.checks:
            button.destroy()

        if self.forward_button:
            self.forward_button.destroy()
        if self.back_button:
            self.back_button.destroy()

        self.selected_actions.clear()
        self.controller.selected_state_id = None
