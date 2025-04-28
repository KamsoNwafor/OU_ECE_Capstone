import tkinter as tk
from tkinter import ttk, messagebox
from Database import DatabaseManager as dbm

class PasswordFrame(tk.Frame):
    frame_index = 2
    is_correct_password = False

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master, bg="#fafafa")  # Set background color for the whole frame
        self.controller = controller

        # Set up database connection and cursor
        self.rds_conn = dbm.get_rds_conn()
        self.rds_cursor = self.rds_conn.cursor()

        self.password_tuple = None  # Will store query results (tuples)
        self.correct_password = None  # Will store the correct password string

        # Prevent frame from resizing based on its content
        self.pack_propagate(False)

        # Configure layout to allow centering of content
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create header section with title
        header = tk.Frame(self, bg="#4CAF50")
        header.pack(fill="x")
        tk.Label(header, text="User Authentication", font=("Roboto", 14, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(pady=10)

        # Create main content area
        content = tk.Frame(self, bg="#f0f0f0", bd=1, relief="solid")
        content.pack(pady=5, padx=5, fill="x", expand=False)

        # Configure layout inside content
        content.grid_rowconfigure(0, weight=0)  # User name display
        content.grid_rowconfigure(1, weight=0)  # Password input
        content.grid_rowconfigure(2, weight=0)  # Navigation buttons
        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=1)

        # Display selected user's name
        self.user_name = tk.Label(content, text="", font=("Roboto", 12, "bold"), bg="#f0f0f0", fg="#212121")
        self.user_name.grid(row=0, column=0, columnspan=2, pady=(10, 5))

        # Password label
        self.user_password = tk.Label(content, text="Enter Your Password:", font=("Roboto", 12), bg="#f0f0f0", fg="#333333")
        self.user_password.grid(row=1, column=0, pady=5, sticky="e")

        # Password entry field (larger text and box)
        self.password_text = tk.StringVar()
        self.password_text.set("")
        self.password_bar = ttk.Entry(content, textvariable=self.password_text, show="*", font=("Roboto", 14))  # Bigger font for password
        self.password_bar.grid(row=1, column=1, pady=5, ipady=4, sticky="w")  # Taller entry with internal padding

        # Navigation buttons (Back and Forward)
        nav_frame = tk.Frame(content, bg="#f0f0f0")
        nav_frame.grid(row=2, column=0, columnspan=2, pady=(8, 2))

        nav_frame.grid_columnconfigure(0, weight=1)
        nav_frame.grid_columnconfigure(1, weight=1)
        nav_frame.grid_columnconfigure(2, weight=1)

        self.back_button = ttk.Button(nav_frame, text="Back", style="Secondary.TButton", command=self.previous_page)
        self.back_button.grid(row=0, column=1, padx=5)

        self.forward_button = ttk.Button(nav_frame, text="Forward", style="Primary.TButton", command=self.password_update)
        self.forward_button.grid(row=0, column=2, padx=5)

    def password_update(self):
        # Validate the entered password
        self.password_check()
        if self.is_correct_password:
            self.controller.frames[3][1].update_task_list()  # Move to the task selection page
            self.controller.forward_button()
        else:
            messagebox.showerror("Incorrect Password", "The password you entered is incorrect. Please try again.", parent=self.controller)

    def password_check(self):
        # Compare entered password with correct password
        try:
            if self.password_text.get() == self.correct_password:
                self.is_correct_password = True
            else:
                self.is_correct_password = False
        except ValueError as e:
            self.is_correct_password = False
            messagebox.showerror("Password Error", f"Error checking password: {str(e)}", parent=self.controller)

    def update_user(self):
        # Load and display the selected user's name
        try:
            self.rds_cursor.execute("SELECT first_name, last_name FROM employees WHERE user_id = %s", (self.controller.selected_user_id,))
            result = self.rds_cursor.fetchall()
            if result:
                employee_name = f"{result[0][0]} {result[0][1]}"
                self.user_name.config(text="Selected User: " + employee_name)
            else:
                print("No user found for user_id:", self.controller.selected_user_id)
        except Exception as e:
            print(f"Error updating user: {e}")

    def load_correct_password(self):
        # Load the correct password for the selected user
        try:
            self.rds_cursor.execute("SELECT password FROM employees WHERE user_id = %s", (self.controller.selected_user_id,))
            self.password_tuple = self.rds_cursor.fetchall()
            if self.password_tuple:
                self.correct_password = self.password_tuple[0][0]
               # print(f"Loaded password for user_id {self.controller.selected_user_id}: {self.correct_password}")
            else:
                print("No password found for user_id:", self.controller.selected_user_id)
        except Exception as e:
            print(f"Error loading password: {e}")

    def previous_page(self):
        # Navigate back to the User selection page
        self.controller.show_page(1)
        self.controller.selected_user_id = None  # Reset selected user
