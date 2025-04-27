

import tkinter as tk
from tkinter import ttk
from Database import DatabaseManager as dbm

class TaskSelectionFrame(tk.Frame):
    frame_index = 3

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master, bg="#fafafa")  # Set soft background color
        self.controller = controller

        self.rds_conn = dbm.get_rds_conn()
        self.rds_cursor = self.rds_conn.cursor()

        self.tasks = None

        # Create header with title
        header = tk.Frame(self, bg="#4CAF50")
        header.pack(fill="x")
        tk.Label(header, text="Step 4: Task Selection", font=("Roboto", 14, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(pady=15)

        # Create content frame
        content = tk.Frame(self, bg="#f0f0f0", bd=1, relief="solid")
        content.pack(pady=10, padx=10, fill="both", expand=True)

        # Instruction label
        self.task_label = tk.Label(content, text="Please select your task", font=("Roboto", 12, "bold"), bg="#f0f0f0", fg="#212121")
        self.task_label.grid(row=0, column=0, pady=(10, 5))

        # Task selection
        self.task_list = tk.StringVar(self)
        self.task_list.set("0")

        self.task_option = None
        self.forward_button = None
        self.back_button = None

    def manage_option(self):
        if self.task_list.get() != "0":
            self.controller.selected_task_id = self.task_list.get()
            self.controller.frames[4][1].load_battery_list()
            self.controller.frames[4][1].bind_double_click()
            self.controller.frames[4][1].update_user()
            self.controller.show_page(4)

    def update_task_list(self):
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
        self.tasks = self.rds_cursor.fetchall()

        # Add radiobuttons to the content frame
        content = self.task_label.master  # Get the content frame (parent of task_label)
        index = 1
        for task in self.tasks:
            self.task_option = ttk.Radiobutton(content, text=task[1], variable=self.task_list, value=task[0])
            self.task_option.grid(row=index, column=0, padx=10, pady=5, sticky="w")
            index += 1

        # Navigation buttons
        nav_frame = tk.Frame(content, bg="#f0f0f0")
        nav_frame.grid(row=index, column=0, pady=10)

        self.back_button = ttk.Button(nav_frame, text="Back", style="Secondary.TButton", command=self.previous_page)
        self.back_button.pack(side="left", padx=5)

        self.forward_button = ttk.Button(nav_frame, text="Forward", style="Primary.TButton", command=self.manage_option)
        self.forward_button.pack(side="left", padx=5)

    def previous_page(self):
        self.controller.frames[2][1].previous_page()
