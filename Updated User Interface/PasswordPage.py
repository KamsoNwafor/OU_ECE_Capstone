import tkinter as tk
from tkinter import ttk, messagebox
from Database import DatabaseManager as dbm

class PasswordFrame(tk.Frame):
    frame_index = 2
    is_correct_password = False

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master, bg="#fafafa")  # Same soft background color as the previous version
        self.controller = controller

        self.rds_conn = dbm.get_rds_conn()  # Same database connection setup as the previous version
        self.rds_cursor = self.rds_conn.cursor()  # Same cursor for database queries

        self.password_tuple = None  # Same null variable for query results (tuples)
        self.correct_password = None  # Same null variable for the password string

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
        tk.Label(header, text="Step 3: Password Entry", font=("Roboto", 14, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(pady=15)  # Same font and padding

        # Content frame is similar but with the same padding as the previous version for consistency.
        content = tk.Frame(self, bg="#f0f0f0", bd=1, relief="solid")
        content.pack(pady=10, padx=10, fill="both", expand=True)  # Same expand behavior

        # NEW: Configure content frame rows and columns to center widgets and make them responsive.
        # This improves scaling compared to the fixed grid positions in the previous version.
        content.grid_rowconfigure(0, weight=1)
        content.grid_rowconfigure(1, weight=1)
        content.grid_rowconfigure(2, weight=1)
        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=1)

        # Selected user label, identical to the previous version in style and placement.
        self.user_name = tk.Label(content, text="", font=("Roboto", 12, "bold"), bg="#f0f0f0", fg="#212121")
        self.user_name.grid(row=0, column=0, columnspan=2, pady=(10, 5))

        # Password label, same as the previous version in style and alignment.
        self.user_password = tk.Label(content, text="Password:", font=("Roboto", 11), bg="#f0f0f0", fg="#333333")
        self.user_password.grid(row=1, column=0, pady=5, sticky="e")

        # Password entry, same functionality but without the external style mentioned in the previous version (TEntry in app.py).
        self.password_text = tk.StringVar()
        self.password_text.set("")
        self.password_bar = ttk.Entry(content, textvariable=self.password_text, show="*")  # Default ttk.Entry styling
        self.password_bar.grid(row=1, column=1, pady=5, sticky="w")  # Same alignment as the previous version

        # Navigation buttons frame, similar to the previous version but using grid for centering.
        nav_frame = tk.Frame(content, bg="#f0f0f0")
        nav_frame.grid(row=2, column=0, columnspan=2, pady=10)

        # NEW: Configure nav_frame columns to center buttons (unlike the pack-based layout in the previous version).
        # This ensures buttons are visually balanced in the UI.
        nav_frame.grid_columnconfigure(0, weight=1)
        nav_frame.grid_columnconfigure(1, weight=1)
        nav_frame.grid_columnconfigure(2, weight=1)

        self.back_button = ttk.Button(nav_frame, text="Back", style="Secondary.TButton", command=self.previous_page)
        self.back_button.grid(row=0, column=1, padx=5)  # Grid instead of pack for precise centering

        self.forward_button = ttk.Button(nav_frame, text="Forward", style="Primary.TButton", command=self.password_update)
        self.forward_button.grid(row=0, column=2, padx=5)  # Grid for consistent alignment

    def password_update(self):
        self.password_check()  # Same password validation logic as the previous version
        if self.is_correct_password:
            self.controller.frames[3][1].update_task_list()  # Same task list update
            self.controller.forward_button()  # Same navigation method
        else:
            messagebox.showerror("Incorrect Password", "The password you entered is incorrect. Please try again.", parent=self.controller)  # Same error message

    def password_check(self):
        try:
            if self.password_text.get() == self.correct_password:
                self.is_correct_password = True
            else:
                self.is_correct_password = False
        except ValueError as e:
            self.is_correct_password = False
            messagebox.showerror("Password Error", f"Error checking password: {str(e)}", parent=self.controller)  # Same error handling

    def update_user(self):
        # NEW: Added try-except to handle database errors (the previous version had no error handling).
        try:
            # Same query as the previous version
            # Uppercase is stylistic; %s may depend on the database driver but is functionally similar.
            self.rds_cursor.execute("SELECT first_name, last_name FROM employees WHERE user_id = %s", (self.controller.selected_user_id,))
            result = self.rds_cursor.fetchall()
            # NEW: Check for empty results to prevent index errors (unlike the previous version).
            if result:
                employee_name = f"{result[0][0]} {result[0][1]}"
                self.user_name.config(text="Selected User: " + employee_name)
            else:
                # NEW: Print for debugging if no user is found (not in the previous version).
                print("No user found for user_id:", self.controller.selected_user_id)
        except Exception as e:
            # NEW: Log errors for debugging (not in the previous version).
            print(f"Error updating user: {e}")

    def load_correct_password(self):
        # NEW: Added try-except to handle database errors (the previous version had no error handling).
        try:
            # Same query as the previous version, but with uppercase SQL and %s placeholder.
            self.rds_cursor.execute("SELECT password FROM employees WHERE user_id = %s", (self.controller.selected_user_id,))
            self.password_tuple = self.rds_cursor.fetchall()
            # NEW: Check for empty results to prevent index errors (unlike the previous version).
            if self.password_tuple:
                self.correct_password = self.password_tuple[0][0]
                # NEW: Print for debugging to confirm password loading (not in the previous version).
                print(f"Loaded password for user_id {self.controller.selected_user_id}: {self.correct_password}")
            else:
                # NEW: Print for debugging if no password is found (not in the previous version).
                print("No password found for user_id:", self.controller.selected_user_id)
        except Exception as e:
            # NEW: Log errors for debugging (not in the previous version).
            print(f"Error loading password: {e}")

    def previous_page(self):
        self.controller.show_page(1)  # Same navigation to UserFrame (index 1)
        self.controller.selected_user_id = None  # Same user ID reset
