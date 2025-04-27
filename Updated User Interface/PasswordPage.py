import tkinter as tk
from tkinter import ttk, messagebox
from Database import DatabaseManager as dbm

class PasswordFrame(tk.Frame):
    frame_index = 2
    is_correct_password = False

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master, bg="#fafafa")  # Set soft background color
        self.controller = controller

        self.rds_conn = dbm.get_rds_conn()  # Connect to RDS database
        self.rds_cursor = self.rds_conn.cursor()  # Create cursor to search through RDS database

        self.password_tuple = None  # All queries return tuples
        self.correct_password = None  # Create a null variable to store the password string

        # Create header with title
        header = tk.Frame(self, bg="#4CAF50")
        header.pack(fill="x")
        tk.Label(header, text="Step 3: Password Entry", font=("Roboto", 14, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(pady=15)

        # Create content frame
        content = tk.Frame(self, bg="#f0f0f0", bd=1, relief="solid")
        content.pack(pady=10, padx=10, fill="both", expand=True)

        # Selected user label
        self.user_name = tk.Label(content, text="", font=("Roboto", 12, "bold"), bg="#f0f0f0", fg="#212121")
        self.user_name.grid(row=0, column=0, columnspan=2, pady=(10, 5))

        # Password label
        self.user_password = tk.Label(content, text="Password:", font=("Roboto", 11), bg="#f0f0f0", fg="#333333")
        self.user_password.grid(row=1, column=0, pady=5, sticky="e")

        # Password entry
        self.password_text = tk.StringVar()
        self.password_text.set("")
        self.password_bar = ttk.Entry(content, textvariable=self.password_text, show="*")  # Font is set via TEntry style in app.py
        self.password_bar.grid(row=1, column=1, pady=5, sticky="w")

        # Navigation buttons
        nav_frame = tk.Frame(content, bg="#f0f0f0")
        nav_frame.grid(row=2, column=0, columnspan=2, pady=10)

        self.back_button = ttk.Button(nav_frame, text="Back", style="Secondary.TButton", command=self.previous_page)
        self.back_button.pack(side="left", padx=5)

        self.forward_button = ttk.Button(nav_frame, text="Forward", style="Primary.TButton", command=self.password_update)
        self.forward_button.pack(side="left", padx=5)

    def password_update(self):
        self.password_check()
        if self.is_correct_password:
            self.controller.frames[3][1].update_task_list()
            self.controller.forward_button()
        else:
            messagebox.showerror("Incorrect Password", "The password you entered is incorrect. Please try again.", parent=self.controller)

    def password_check(self):
        try:
            if self.password_text.get() == self.correct_password:
                self.is_correct_password = True
            else:
                self.is_correct_password = False
        except ValueError as e:
            self.is_correct_password = False
            messagebox.showerror("Password Error", f"Error checking password: {str(e)}", parent=self.controller)

    def update_user(self):
        self.rds_cursor.execute("select first_name, last_name from employees where user_id = ?", (self.controller.selected_user_id,))
        result = self.rds_cursor.fetchall()
        employee_name = f"{result[0][0]} {result[0][1]}"
        self.user_name.config(text="Selected User: " + employee_name)

    def load_correct_password(self):
        self.rds_cursor.execute("select password from employees where user_id = ?", (self.controller.selected_user_id,))
        self.password_tuple = self.rds_cursor.fetchall()
        self.correct_password = self.password_tuple[0][0]

    def previous_page(self):
        self.controller.show_page(1)
        self.controller.selected_user_id = None
