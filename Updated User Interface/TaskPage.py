import tkinter as tk
from Database import DatabaseManager

# TODO: Add Switch Case in manage_option()

# import the tk.Frame class that creates frames
class TaskFrame(tk.Frame):
    def __init__(self, master, controller): # initialise the imported class
        tk.Frame.__init__(self, master)

        self.tasks = DatabaseManager.get_tasks() # retrieves usernames in database

        self.controller = controller # store an instance of controller in frame, easier to manage controller data

        self.task_label = tk.Label(master = self) # create instruction label
        self.task_label.config(text = "Please select your task")
        self.task_label.grid(row = 0, column  = 1) # place instruction label in top-centre area of frame

        self.task_list = tk.StringVar(master = self) # String Variable to store button options
        self.task_list.set("0") # Initial value must be different from options listed in order to avoid selection errors

        index = 1
        for task in self.tasks:
            self.task_option = tk.Radiobutton(master = self) # creates a single-selection list for each task
            self.task_option.config(text = task, variable = self.task_list, value = index) # labels each choice by the relevant task and gives it a place value
            self.task_option.grid(row = index, column = 1, padx=10, pady=10, sticky="NEWS") # place the choices in the centre, one after the other
            index += 1

        self.forward_button = tk.Button(master=self)  # button to go to the next page (password page)
        self.forward_button.config(width=20, text="Forward", command=lambda: self.manage_option()) # manages the option when clicked, next frame is based on switch-case
        self.forward_button.grid(row=index, column=2, padx=10, pady=10, sticky="SE") # places forward button at the bottom right of screen

        self.back_button = tk.Button(master=self)  # button to go to the next page (password page)
        self.back_button.config(width=20, text="Back", command=lambda: controller.back_button())
        self.back_button.grid(row=index, column=0, padx=10, pady=10, sticky="SW") # places back button at the bottom left of screen

    def manage_option(self):
        self.controller.selected_task = self.task_list.get() # save the selected task's value (work_type_id)
        self.controller.forward_button() # replace with switch case to choose next frame