import tkinter as tk
from tkinter import ttk
from Database import DatabaseManager as dbm

class UserFrame(tk.Frame):
    chosen_user = None
    frame_index = 1

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master, bg="#fafafa")  # Same soft background color as the previous version
        self.controller = controller

        self.rds_conn = dbm.get_rds_conn()  # Same database connection setup as the previous version
        self.rds_cursor = self.rds_conn.cursor()  # Same cursor for database queries

        self.users = None  # Null variable for users, same as the previous version
        self.filtered_users = []  # Array for filtered user names in the listbox
        self.filtered_user_ids = []  # Array for corresponding user IDs

        # NEW: Prevent the frame from resizing based on its content (unlike the previous version, which used pack without this).
        # This ensures better control over layout and keeps widgets centered.
        self.pack_propagate(False)

        # NEW: Configure the frame to expand and center content by assigning weight to row/column 0.
        # This makes the UI responsive to window resizing, unlike the fixed grid in the previous version.
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Same header frame with green background, but with smaller padding and font for a more compact design.
        header = tk.Frame(self, bg="#4CAF50")
        header.pack(fill="x")  # Same horizontal fill as the previous version
        tk.Label(header, text="Step 2: User Selection", font=("Roboto", 12, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(pady=10)  # Smaller font (12 vs 14) and padding (10 vs 15) than the previous version

        # Content frame is similar but with reduced padding (5 vs 10) for a tighter layout compared to the previous version.
        content = tk.Frame(self, bg="#f0f0f0", bd=1, relief="solid")
        content.pack(pady=5, padx=5, fill="both", expand=True)  # Still expands like the previous version

        # NEW: Configure content frame rows and columns to center widgets and make them responsive.
        # This improves scaling compared to the fixed grid positions in the previous version.
        content.grid_rowconfigure(0, weight=1)
        content.grid_rowconfigure(1, weight=1)
        content.grid_rowconfigure(2, weight=1)
        content.grid_rowconfigure(3, weight=1)
        content.grid_rowconfigure(4, weight=1)
        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=1)
        content.grid_columnconfigure(2, weight=1)

        # Username label, same as the previous version but with smaller font (9 vs 11) for a more compact look.
        self.user_name = tk.Label(content, text="Username:", font=("Roboto", 13), bg="#f0f0f0", fg="#333333")
        self.user_name.grid(row=0, column=1, pady=(3, 2))  # Reduced padding compared to the previous version

        # Username entry, same functionality but without the external style mentioned in the previous version (TEntry in app.py).
        self.employee = tk.StringVar()
        self.employee.set("")
        self.name_bar = ttk.Entry(content, textvariable=self.employee)
        self.name_bar.grid(row=1, column=1, pady=2, sticky="ew")  # NEW: sticky="ew" makes the entry expand horizontally, unlike the previous version
        self.name_bar.bind('<KeyRelease>', self.check_key)  # Same key release binding to filter users

        # Scrollbar and listbox setup, similar to the previous version but with explicit size (height=3, width=20) for compactness.
        self.user_scrollbar = tk.Scrollbar(content, orient="vertical")
        self.user_scrollbar.grid(row=2, column=2, padx=(0, 5), pady=5, sticky="NS")  # Same vertical alignment as the previous version

        self.user_list = tk.Listbox(content, yscrollcommand=self.user_scrollbar.set, font=("Roboto", 11), height=4, width=20)  # Smaller font and fixed size compared to the previous version's default size
        self.user_scrollbar.config(command=self.user_list.yview)
        self.user_list.bind("<Double-1>", self.user_selection)  # Same double-click binding as the previous version
        self.user_list.grid(row=2, column=1, padx=5, pady=5, sticky="ew")  # NEW: sticky="ew" for horizontal expansion, unlike the previous version

        # NEW: Load users from database immediately, but don't populate the listbox yet (unlike the previous version, which called list_update).
        # This delays listbox population until the user types, reducing initial load time.
        self.load_user_list()

        # Missing name instruction, same as the previous version but with smaller font (9 vs 11).
        self.missing_name = tk.Label(content, text="If your name is not listed, please contact your supervisor", font=("Roboto", 13), bg="#f0f0f0", fg="#333333")
        self.missing_name.grid(row=3, column=1, pady=2)  # Reduced padding compared to the previous version

        # Navigation buttons frame, similar to the previous version but using grid for precise centering.
        nav_frame = tk.Frame(content, bg="#f0f0f0")
        nav_frame.grid(row=4, column=0, columnspan=3, pady=1)

        # NEW: Configure nav_frame columns to center buttons (unlike the pack-based layout in the previous version).
        nav_frame.grid_columnconfigure(0, weight=1)
        nav_frame.grid_columnconfigure(1, weight=1)
        nav_frame.grid_columnconfigure(2, weight=1)

        self.back_button = ttk.Button(nav_frame, text="Back", style="Secondary.TButton", command=self.previous_page)
        self.back_button.grid(row=0, column=1, padx=3)  # Grid instead of pack for better alignment compared to the previous version

        self.forward_button = ttk.Button(nav_frame, text="Forward", style="Primary.TButton", command=lambda: self.user_selection(None))
        self.forward_button.grid(row=0, column=2, padx=3)  # Grid for precise placement, unlike the previous version

    def check_key(self, event):
        value = self.employee.get()
        # NEW: Added print statement for debugging to track the entry value (not present in the previous version).
        print(f"Entry value: {value}")

        # NEW: Check if the users list is empty to avoid errors (the previous version assumed users was populated).
        if not self.users:
            print("Users list is empty")
            self.filtered_users = []
            self.filtered_user_ids = []
        elif value == '':
            self.filtered_users = []
            self.filtered_user_ids = []
        else:
            self.filtered_users = []
            self.filtered_user_ids = []
            for item in self.users:
                full_name = f"{item[1]} {item[2]}"  # Same name filtering logic as the previous version
                if value.lower() in full_name.lower():
                    self.filtered_users.append(full_name)
                    self.filtered_user_ids.append(item[0])

        # NEW: Print filtered users for debugging (not in the previous version).
        print(f"Filtered users: {self.filtered_users}")
        self.list_update(self.filtered_users)  # Same list update call as the previous version

    def list_update(self, data):
        self.user_list.delete(0, 'end')
        for item in data:
            self.user_list.insert('end', item)
        # NEW: Print to confirm listbox updates (not in the previous version).
        print(f"Listbox updated with: {data}")

    def user_selection(self, event):
        if self.filtered_users and self.user_list.curselection():
            index = self.user_list.curselection()[0]
            for i in self.user_list.curselection():
                self.employee.set(self.user_list.get(i))

            self.chosen_user = self.filtered_users[index]
            self.controller.selected_user_id = self.filtered_user_ids[index]

            self.controller.frames[2][1].update_user()
            self.controller.frames[2][1].load_correct_password()
            # NEW: Explicitly navigate to PasswordFrame (index 2) instead of the previous version's forward_button().
            # This ensures clear and predictable page transitions.
            self.controller.show_page(2)  # Unlike the previous version, no list_update to keep the filtered list intact

    def load_user_list(self):
        # NEW: Added try-except to handle database errors (the previous version had no error handling).
        try:
            # Same query as the previous version, but with uppercase SQL keywords for readability (functionally identical).
            self.rds_cursor.execute("SELECT user_id, first_name, last_name FROM employees")
            self.users = self.rds_cursor.fetchall()
            # NEW: Print loaded users for debugging (not in the previous version).
            print(f"Loaded users: {self.users}")
        except Exception as e:
            # NEW: Handle errors by setting users to an empty list and logging the issue.
            print(f"Error loading users from database: {e}")
            self.users = []

    def previous_page(self):
        self.controller.show_page(0)  # Same as the previous version, navigates to the previous page
