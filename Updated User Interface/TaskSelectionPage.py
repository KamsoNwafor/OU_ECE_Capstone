import tkinter as tk
from tkinter import ttk
from Database import DatabaseManager as dbm

class TaskSelectionFrame(tk.Frame):
    frame_index = 3

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master, bg="#fafafa")  # Same soft background color as the previous version
        self.controller = controller

        self.rds_conn = dbm.get_rds_conn()  # Same database connection setup as the previous version
        self.rds_cursor = self.rds_conn.cursor()  # Same cursor for database queries

        self.tasks = None  # Same null variable for tasks

        # NEW: Prevent the frame from resizing based on its content (unlike the previous version, which used pack without this).
        # This ensures better control over layout and keeps widgets centered.
        self.pack_propagate(False)

        # NEW: Configure the frame to expand and center content by assigning weight to row/column 0.
        # This makes the UI responsive to window resizing, unlike the fixed layout in the previous version.
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Same header frame with green background, identical to the previous version.
        header = tk.Frame(self, bg="#4CAF50")
        header.pack(fill="x")  # Same horizontal fill
        tk.Label(header, text="Step 4: Task Selection", font=("Roboto", 14, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(pady=15)  # Same font and padding

        # Content frame is similar with the same padding as the previous version for consistency.
        content = tk.Frame(self, bg="#f0f0f0", bd=1, relief="solid")
        content.pack(pady=10, padx=10, fill="both", expand=True)  # Same expand behavior

        # NEW: Configure content frame rows and columns to center widgets and make them responsive.
        # Pre-configure up to 10 rows to accommodate dynamic radiobuttons, unlike the previous version's dynamic grid.
        content.grid_rowconfigure(0, weight=1)
        for i in range(1, 10):  # Assuming up to 9 tasks for now
            content.grid_rowconfigure(i, weight=1)
        content.grid_columnconfigure(0, weight=1)

        # Instruction label, identical to the previous version in style and placement.
        self.task_label = tk.Label(content, text="Please select your task", font=("Roboto", 12, "bold"), bg="#f0f0f0", fg="#212121")
        self.task_label.grid(row=0, column=0, pady=(10, 5))

        # Task selection, same setup as the previous version.
        self.task_list = tk.StringVar(self)
        self.task_list.set("0")

        self.task_option = None  # Same placeholder for radiobutton
        self.forward_button = None  # Same placeholder for forward button
        self.back_button = None  # Same placeholder for back button

        # NEW: Load tasks immediately at initialization (unlike the previous version, which deferred update_task_list).
        # This pre-loads tasks for faster display when the frame is shown.
        self.update_task_list()

    def manage_option(self):
        if self.task_list.get() != "0":
            self.controller.selected_task_id = self.task_list.get()  # Same task ID assignment
            self.controller.frames[4][1].load_battery_list()  # Same battery list load
            self.controller.frames[4][1].bind_double_click()  # Same binding
            self.controller.frames[4][1].update_user()  # Same user update
            self.controller.show_page(4)  # Same navigation to next frame
        else:
            # NEW: Print for debugging when no task is selected (the previous version silently did nothing).
            print("No task selected")

    def update_task_list(self):
        # NEW: Added try-except to handle database errors (the previous version had no error handling).
        try:
            # Same query as the previous version, but with uppercase SQL keywords for readability (functionally identical).
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
            # NEW: Print loaded tasks for debugging (not in the previous version).
            print(f"Loaded tasks: {self.tasks}")
        except Exception as e:
            # NEW: Handle errors by setting tasks to an empty list and logging the issue.
            print(f"Error loading tasks from database: {e}")
            self.tasks = []

        # NEW: Check for empty tasks to prevent displaying an empty UI (not in the previous version).
        if not self.tasks:
            print("No tasks available to display")
            return

        # Add radiobuttons, same as the previous version but within the responsive grid.
        content = self.task_label.master
        index = 1
        for task in self.tasks:
            self.task_option = ttk.Radiobutton(content, text=task[1], variable=self.task_list, value=task[0],)
            self.task_option.grid(row=index, column=0, padx=10, pady=5)  # Same placement and styling
            index += 1

        # Navigation buttons frame, similar to the previous version but using grid for centering.
        nav_frame = tk.Frame(content, bg="#f0f0f0")
        nav_frame.grid(row=index, column=0, pady=10)

        # NEW: Configure nav_frame columns to center buttons (unlike the pack-based layout in the previous version).
        # This ensures buttons are visually balanced in the UI.
        nav_frame.grid_columnconfigure(0, weight=1)
        nav_frame.grid_columnconfigure(1, weight=1)
        nav_frame.grid_columnconfigure(2, weight=1)

        self.back_button = ttk.Button(nav_frame, text="Back", style="Secondary.TButton", command=self.previous_page)
        self.back_button.grid(row=0, column=1, padx=5)  # Grid instead of pack for precise centering

        self.forward_button = ttk.Button(nav_frame, text="Forward", style="Primary.TButton", command=self.manage_option)
        self.forward_button.grid(row=0, column=2, padx=5)  # Grid for consistent alignment

    def previous_page(self):
        self.controller.frames[2][1].previous_page()
