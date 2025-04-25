import tkinter as tk
from Database import DatabaseManager as dbm

# import the tk.Frame class that creates frames
class TaskSelectionFrame(tk.Frame):
    # store relative frame index number
    frame_index = 3

    def __init__(self, master, controller):
        # initialise the imported class
        tk.Frame.__init__(self, master)

        # connect to database and create cursor to traverse through database
        self.rds_conn = dbm.get_rds_conn()
        self.rds_cursor = self.rds_conn.cursor()

        # empty variable to store task names
        self.tasks = None

        # store an instance of controller in frame, easier to manage controller data
        self.controller = controller

        # create instruction label and place instruction label in top-centre area of frame
        self.task_label = tk.Label(master = self)
        self.task_label.config(text = "Please select your task")
        self.task_label.grid(row = 0, column  = 1)

        # String Variable to store button options
        # Initial value must be different from options listed in order to avoid selection errors
        self.task_list = tk.StringVar(master = self)
        self.task_list.set("0")

        # task option tracker variable.
        # Don't initialise positions of buttons, as they depend on the tracker variable
        self.task_option = None
        self.forward_button = None
        self.back_button = None

    def manage_option(self):
        # save the selected task's value (work_type_id)
        self.controller.selected_task_id = self.task_list.get()

        # loads battery list and updates the user on the battery selection page
        self.controller.frames[4][1].load_battery_list()
        self.controller.frames[4][1].update_user()
        self.controller.forward_button()

    def update_task_list(self):

        # searches for the main tasks wanted listed by spiers in the database
        self.rds_cursor.execute("""
        select work_type_id, work_type_name
        from works
        where parent_work_type_id is null  
        union
        select work_type_id, work_type_name
        from works
        where parent_work_type_id = 1
        order by work_type_id;
        """)

        # loads the main tasks into the task selection list
        self.tasks = self.rds_cursor.fetchall()

        index = 1
        for task in self.tasks:
            # creates a single-selection list for each task
            self.task_option = tk.Radiobutton(master=self)

            # labels each choice by the relevant task and gives it a place value
            self.task_option.config(text=task[1], variable=self.task_list, value=task[0])

            # place the choices in the centre, one after the other
            self.task_option.grid(row=index, column=1, padx=10, pady=10,
                                  sticky="NEWS")
            index += 1

        # button to go to the next page (item selection page)
        # the button saves the task id selected and goes to the next page when clicked
        self.forward_button = tk.Button(master=self)
        self.forward_button.config(width=20, text="Forward", command=lambda: self.manage_option())

        # place the forward button at the bottom right of screen
        self.forward_button.grid(row=index, column=2, padx=10, pady=10, sticky="SE")

        # button to go to the previous logical page (user page, jumps past password page)
        self.back_button = tk.Button(master=self)
        self.back_button.config(width=20, text="Back", command=lambda: self.controller.show_page(1))

        # places back button at the bottom left of screen
        self.back_button.grid(row=index, column=0, padx=10, pady=10, sticky="SW")

