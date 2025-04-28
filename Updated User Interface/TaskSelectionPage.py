import tkinter as tk
from tkinter import ttk
from Database import DatabaseManager as dbm

class TaskSelectionFrame(tk.Frame):
    frame_index = 3

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master, bg="#fafafa")  # Set background color
        self.controller = controller

        # Set up database connection and cursor
        self.rds_conn = dbm.get_rds_conn()
        self.rds_cursor = self.rds_conn.cursor()

        self.tasks = None  # Will store list of tasks fetched from database

        # Prevent frame from resizing based on content
        self.pack_propagate(False)

        # Configure layout to allow centering
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create header section with title
        header = tk.Frame(self, bg="#4CAF50")
        header.pack(fill="x")
        tk.Label(header, text="Step 4: Task Selection", font=("Roboto", 14, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(pady=10)

        # Create main content area
        content = tk.Frame(self, bg="#f0f0f0", bd=1, relief="solid")
        content.pack(pady=5, padx=5, fill="x", expand=False)

        # Configure content grid for two columns
        content.grid_rowconfigure(0, weight=0)
        for i in range(1, 10):  # Reserve rows for tasks
            content.grid_rowconfigure(i, weight=0)
        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=1)

        # Instruction label
        self.task_label = tk.Label(content, text="Please select your task", font=("Roboto", 12, "bold"), bg="#f0f0f0", fg="#212121")
        self.task_label.grid(row=0, column=0, columnspan=2, pady=(10, 5))

        # Setup for task selection
        self.task_list = tk.StringVar(self)
        self.task_list.set("0")

        self.task_option = None  # Placeholder for radiobuttons
        self.forward_button = None  # Placeholder for forward button
        self.back_button = None  # Placeholder for back button

        # Load available tasks
        self.update_task_list()

    def manage_option(self):
        # Proceed if a task is selected, otherwise print warning
        if self.task_list.get() != "0":
            self.controller.selected_task_id = self.task_list.get()
            self.controller.frames[4][1].load_battery_list()
            self.controller.frames[4][1].bind_double_click()
            self.controller.frames[4][1].update_user()
            self.controller.show_page(4)
        else:
            print("No task selected")

    def update_task_list(self):
        # Fetch task list from database
        try:
            self.rds_cursor.execute("""
            SELECT work_type_id, work_type_name
            FROM works
            WHERE parent_work_type_id IS NULL
            UNION
            SELECT work_type_id, work_type_name
            FROM works
            WHERE parent_work_type_id = 1
            ORDER BY work_type_id;
            """)
            self.tasks = self.rds_cursor.fetchall()
            print(f"Loaded tasks: {self.tasks}")
        except Exception as e:
            print(f"Error loading tasks from database: {e}")
            self.tasks = []

        if not self.tasks:
            print("No tasks available to display")
            return

        # Create Radiobuttons for each task
        content = self.task_label.master
        split_point = (len(self.tasks) + 1) // 2  # Calculate halfway point

        for index, task in enumerate(self.tasks):
            if index < split_point:
                row = index + 1
                column = 0
            else:
                row = index - split_point + 1
                column = 1

            self.task_option = ttk.Radiobutton(content, text=task[1], variable=self.task_list, value=task[0])
            self.task_option.grid(row=row, column=column, padx=10, pady=3, sticky="w")

        # Create navigation buttons frame
        nav_frame = tk.Frame(content, bg="#f0f0f0")
        nav_frame.grid(row=max(split_point, len(self.tasks) - split_point) + 1, column=0, columnspan=2, pady=(8, 2))

        nav_frame.grid_columnconfigure(0, weight=1)
        nav_frame.grid_columnconfigure(1, weight=1)
        nav_frame.grid_columnconfigure(2, weight=1)

        self.back_button = ttk.Button(nav_frame, text="Back", style="Secondary.TButton", command=self.previous_page)
        self.back_button.grid(row=0, column=1, padx=5)

        self.forward_button = ttk.Button(nav_frame, text="Forward", style="Primary.TButton", command=self.manage_option)
        self.forward_button.grid(row=0, column=2, padx=5)

    def previous_page(self):
        # Navigate back to Password entry frame
        self.controller.frames[2][1].previous_page()
