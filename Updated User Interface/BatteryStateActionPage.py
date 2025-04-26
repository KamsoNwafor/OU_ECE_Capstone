import tkinter as tk
from Database import DatabaseManager as dbm

# import the tk.Frame class that creates frames
class BatteryStateActionFrame(tk.Frame):
    # store relative frame index number
    frame_index = 11

    new_battery = 6
    old_battery = 7
    death_row_battery = 8

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)

        self.controller = controller

        self.actions = None

        self.rds_conn = dbm.get_rds_conn()  # connect to local database
        self.rds_cursor = self.rds_conn.cursor()  # create cursor to search through local database

        self.action_check = None
        self.forward_button = None
        self.back_button = None

        self.battery_action = None

        self.action_prompt = tk.Label (master = self)
        self.action_prompt.config(text = "Please Select the Actions You Have Completed")
        self.action_prompt.grid(row = 0, column = 1)

        self.action_vars = []
        self.selected_actions = []
        self.checks = []

    def finalise_list(self):
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
                                WHERE parent_work_type_id = ?
                                ORDER BY work_type_id
                                """, (self.battery_action,))

        self.actions = self.rds_cursor.fetchall()

        index = 1
        for action in self.actions:
            action_var = tk.IntVar()
            self.action_check = tk.Checkbutton(master = self)
            self.action_check.config(text = action[1], onvalue = action[0], offvalue=0, variable = action_var,
                                     command = lambda: self.update_actions_list())
            self.action_check.grid(row = index, column = 1)
            self.action_vars.append(action_var)
            self.checks.append(self.action_check)
            index += 1

        # creates button to go to the next page (selected task), places forward button at the bottom right of screen
        # if a list item is highlighted, then the forward button is clicked, select it
        self.forward_button = tk.Button(master=self)
        self.forward_button.config(width=20, text="Forward", command=lambda: self.finalise_list())
        self.forward_button.grid(row=index, column=3, padx=10, pady=10, sticky="SE")

        # button to go to the previous page (battery state page), places back button at the bottom left of screen
        self.back_button = tk.Button(master=self)
        self.back_button.config(width=20, text="Back", command=lambda: self.previous_page())
        self.back_button.grid(row=index, column=0, padx=10, pady=10, sticky="SW")

    def update_actions_list(self):
        self.selected_actions.clear()

        for action_var in self.action_vars:
            if action_var.get() != 0:
                self.selected_actions.append(action_var.get())

    def previous_page(self):
        self.controller.show_page(10)

        for button in self.checks:
            button.deselect()
            button.destroy()

        self.forward_button.destroy()
        self.back_button.destroy()

        self.selected_actions.clear()
        self.controller.selected_state_id = None


