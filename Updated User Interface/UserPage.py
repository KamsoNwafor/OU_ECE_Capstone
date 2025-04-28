import tkinter as tk
from tkinter import ttk
from Database import DatabaseManager as dbm

class UserFrame(tk.Frame):
    chosen_user = None
    frame_index = 1

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master, bg="#fafafa")  # Set background color for the whole frame
        self.controller = controller

        # Set up database connection and cursor
        self.rds_conn = dbm.get_rds_conn()
        self.rds_cursor = self.rds_conn.cursor()

        self.users = None  # Will hold all users from the database
        self.filtered_users = []  # Filtered user names for search
        self.filtered_user_ids = []  # Filtered user IDs matching search

        # Prevent frame from resizing based on content
        self.pack_propagate(False)

        # Configure layout to allow centering of content
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create header section with title
        header = tk.Frame(self, bg="#4CAF50")
        header.pack(fill="x")
        tk.Label(header, text="User Selection", font=("Roboto", 12, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(pady=8)

        # Create main content area
        content = tk.Frame(self, bg="#f0f0f0", bd=1, relief="solid")
        content.pack(pady=5, padx=5, fill="x", expand=False)

        # Configure layout inside content
        content.grid_rowconfigure(0, weight=0)  # Username label row
        content.grid_rowconfigure(1, weight=0)  # Username entry row
        content.grid_rowconfigure(2, weight=1)  # Listbox expands
        content.grid_rowconfigure(3, weight=0)  # Missing name message
        content.grid_rowconfigure(4, weight=0)  # Navigation buttons
        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=1)
        content.grid_columnconfigure(2, weight=1)

        # Create Username label
        self.user_name = tk.Label(content, text="Who are you?", font=("Roboto", 13), bg="#f0f0f0", fg="#333333")
        self.user_name.grid(row=0, column=1, pady=(3, 1))

        # Create entry field for typing username
        self.employee = tk.StringVar()
        self.employee.set("")
        self.name_bar = ttk.Entry(content, textvariable=self.employee, font=("Roboto", 14))  # Bigger font
        self.name_bar.grid(row=1, column=1, pady=2,ipady = 4, sticky="ew")
        self.name_bar.bind('<KeyRelease>', self.check_key)

        # Create Listbox with vertical scrollbar
        self.user_scrollbar = tk.Scrollbar(content, orient="vertical")
        self.user_scrollbar.grid(row=2, column=2, padx=(0, 5), pady=2, sticky="NS")

        self.user_list = tk.Listbox(content, yscrollcommand=self.user_scrollbar.set, font=("Roboto", 11), height=4, width=20)
        self.user_scrollbar.config(command=self.user_list.yview)
        self.user_list.bind("<Double-1>", self.user_selection)
        self.user_list.grid(row=2, column=1, padx=5, pady=2, sticky="ew")

        # Load users from database into internal list
        self.load_user_list()

        # Display a help message if user is missing
        self.missing_name = tk.Label(content, text="If your name is not listed, please contact your supervisor",
                                     font=("Roboto", 11), bg="#f0f0f0", fg="#333333")
        self.missing_name.grid(row=3, column=1, pady=2)

        # Create navigation buttons (Back and Forward)
        nav_frame = tk.Frame(content, bg="#f0f0f0")
        nav_frame.grid(row=4, column=0, columnspan=3, pady=(4, 2))

        nav_frame.grid_columnconfigure(0, weight=1)
        nav_frame.grid_columnconfigure(1, weight=1)
        nav_frame.grid_columnconfigure(2, weight=1)

        self.back_button = ttk.Button(nav_frame, text="Back", style="Secondary.TButton", command=self.previous_page)
        self.back_button.grid(row=0, column=1, padx=3)

        self.forward_button = ttk.Button(nav_frame, text="Forward", style="Primary.TButton", command=lambda: self.user_selection(None))
        self.forward_button.grid(row=0, column=2, padx=3)

    def check_key(self, event):
        # Filter the list of users based on typed input
        value = self.employee.get()
      #  print(f"Entry value: {value}")

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
                full_name = f"{item[1]} {item[2]}"
                if value.lower() in full_name.lower():
                    self.filtered_users.append(full_name)
                    self.filtered_user_ids.append(item[0])

      #  print(f"Filtered users: {self.filtered_users}")
        self.list_update(self.filtered_users)

    def list_update(self, data):
        # Update the Listbox with filtered users
        self.user_list.delete(0, 'end')
        for item in data:
            self.user_list.insert('end', item)
      #  print(f"Listbox updated with: {data}")

    def user_selection(self, event):
        # Handle user selection and navigate to the next page
        if self.filtered_users and self.user_list.curselection():
            index = self.user_list.curselection()[0]
            for i in self.user_list.curselection():
                self.employee.set(self.user_list.get(i))

            self.chosen_user = self.filtered_users[index]
            self.controller.selected_user_id = self.filtered_user_ids[index]

            self.controller.frames[2][1].update_user()
            self.controller.frames[2][1].load_correct_password()
            self.controller.show_page(2)

    def load_user_list(self):
        # Load all users from the database into internal memory
        try:
            self.rds_cursor.execute("SELECT user_id, first_name, last_name FROM employees")
            self.users = self.rds_cursor.fetchall()
          #  print(f"Loaded users: {self.users}")
        except Exception as e:
        #    print(f"Error loading users from database: {e}")
            self.users = []

    def previous_page(self):
        # Navigate back to the previous page
        self.controller.show_page(0)
