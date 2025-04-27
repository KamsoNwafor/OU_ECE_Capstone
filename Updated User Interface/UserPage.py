import tkinter as tk
from tkinter import ttk
from Database import DatabaseManager as dbm

class UserFrame(tk.Frame):
    chosen_user = None
    frame_index = 1

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master, bg="#fafafa")  # Set soft background color
        self.controller = controller

        self.rds_conn = dbm.get_rds_conn()  # Connect to RDS database
        self.rds_cursor = self.rds_conn.cursor()  # Create cursor to search through RDS database

        self.users = None  # Create a null variable to store the users
        self.filtered_users = []  # Creates array to store filtered users in drop-down list
        self.filtered_user_ids = []  # Creates array to store filtered user IDs

        # Create header with title
        header = tk.Frame(self, bg="#4CAF50")
        header.pack(fill="x")
        tk.Label(header, text="Step 2: User Selection", font=("Roboto", 14, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(pady=15)

        # Create content frame
        content = tk.Frame(self, bg="#f0f0f0", bd=1, relief="solid")
        content.pack(pady=10, padx=10, fill="both", expand=True)

        # Username label
        self.user_name = tk.Label(content, text="Username:", font=("Roboto", 11), bg="#f0f0f0", fg="#333333")
        self.user_name.grid(row=0, column=1, pady=(10, 5))

        # Username entry
        self.employee = tk.StringVar()
        self.employee.set("")
        self.name_bar = ttk.Entry(content, textvariable=self.employee)  # Font is set via TEntry style in app.py
        self.name_bar.grid(row=1, column=1, pady=5)
        self.name_bar.bind('<KeyRelease>', self.check_key)  # Filters the list every time a key is pressed

        # User list with scrollbar
        self.user_scrollbar = tk.Scrollbar(content, orient="vertical")
        self.user_scrollbar.grid(row=2, column=2, padx=(0, 10), pady=10, sticky="NS")

        self.user_list = tk.Listbox(content, yscrollcommand=self.user_scrollbar.set, font=("Roboto", 11))
        self.user_scrollbar.config(command=self.user_list.yview)
        self.user_list.bind("<Double-1>", self.user_selection)
        self.user_list.grid(row=2, column=1, padx=10, pady=10)
        self.list_update(self.filtered_users)  # Start with empty list

        # Missing name instruction
        self.missing_name = tk.Label(content, text="If your name is not listed, please contact your supervisor", font=("Roboto", 11), bg="#f0f0f0", fg="#333333")
        self.missing_name.grid(row=3, column=1, pady=5)

        # Navigation buttons
        nav_frame = tk.Frame(content, bg="#f0f0f0")
        nav_frame.grid(row=4, column=0, columnspan=3, pady=10)

        self.back_button = ttk.Button(nav_frame, text="Back", style="Secondary.TButton", command=self.previous_page)
        self.back_button.pack(side="left", padx=5)

        self.forward_button = ttk.Button(nav_frame, text="Forward", style="Primary.TButton", command=lambda: self.user_selection(None))
        self.forward_button.pack(side="left", padx=5)

    def check_key(self, event):
        value = event.widget.get()  # Gets the text currently in the entry box

        # If text is empty, empty the list
        if value == '':
            self.filtered_users = []
            self.filtered_user_ids = []
        else:
            self.filtered_users = []
            self.filtered_user_ids = []
            for item in self.users:
                if value.lower() in f"{item[1]} {item[2]}".lower():
                    self.filtered_users.append(f"{item[1]} {item[2]}")
                    self.filtered_user_ids.append(item[0])

        self.list_update(self.filtered_users)

    def list_update(self, data):
        self.user_list.delete(0, 'end')
        for item in data:
            self.user_list.insert('end', item)

    def user_selection(self, event):
        if self.filtered_users and self.user_list.curselection():
            index = self.user_list.curselection()[0]
            for i in self.user_list.curselection():
                self.employee.set(self.user_list.get(i))

            self.chosen_user = self.filtered_users[index]
            self.controller.selected_user_id = self.filtered_user_ids[index]

            self.controller.frames[2][1].update_user()
            self.controller.frames[2][1].load_correct_password()
            self.controller.forward_button()

            data = [self.chosen_user]
            self.list_update(data)

    def load_user_list(self):
        self.rds_cursor.execute("select user_id, first_name, last_name from employees")
        self.users = self.rds_cursor.fetchall()

    def previous_page(self):
        self.controller.show_page(0)
