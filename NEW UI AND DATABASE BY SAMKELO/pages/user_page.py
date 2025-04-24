import tkinter as tk
from tkinter import ttk, messagebox

class UserPage(tk.Frame):
    # Initialize the User Login Page
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#fafafa")
        self.controller = controller

        # Create header with title
        header = tk.Frame(self, bg="#4CAF50")
        header.pack(fill="x")
        tk.Label(header, text="Step 1: Technician Login", font=("Roboto", 14, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(pady=15)

        # Create content frame
        content = tk.Frame(self, bg="#f0f0f0", bd=1, relief="solid")
        content.pack(pady=10, padx=10, fill="both", expand=True)
        tk.Label(content, text="Please log in:", font=("Roboto", 12, "bold"), bg="#f0f0f0", fg="#212121").pack(pady=10)

        # User ID input
        tk.Label(content, text="User ID:", font=("Roboto", 11), bg="#f0f0f0", fg="#333333").pack(pady=5)
        user_id_entry = ttk.Entry(content, textvariable=self.controller.user_id_var, font=("Roboto", 11))
        user_id_entry.pack(pady=5, fill="x", padx=10)
        user_id_entry.focus_set()  # Set focus on User ID field

        # Password input
        tk.Label(content, text="Password:", font=("Roboto", 11), bg="#f0f0f0", fg="#333333").pack(pady=5)
        password_entry = ttk.Entry(content, textvariable=self.controller.password_var, font=("Roboto", 11), show="*")
        password_entry.pack(pady=5, fill="x", padx=10)

        # Navigation buttons
        nav_frame = tk.Frame(content, bg="#f0f0f0")
        nav_frame.pack(pady=10)
        back_btn = ttk.Button(nav_frame, text="Back", style="Secondary.TButton", command=lambda: self.controller.go_back("UserPage"))
        back_btn.pack(side="left", padx=5)
        next_btn = ttk.Button(nav_frame, text="Next", style="Primary.TButton", command=self.validate_and_proceed)
        next_btn.pack(side="left", padx=5)

    # Validate user credentials and proceed
    def validate_and_proceed(self):
        user_id = self.controller.user_id_var.get().strip()
        password = self.controller.password_var.get().strip()
        if not user_id or not password:
            messagebox.showerror("Missing Information", "Please enter both User ID and Password", parent=self.controller.root)
            return

        try:
            if self.controller.db_manager.authenticate_user(user_id, password):
                self.controller.show_frame("LocationPage")  # Proceed to next page
            else:
                messagebox.showerror("Authentication Failed", "Invalid User ID or Password", parent=self.controller.root)
                self.controller.password_var.set("")  # Clear password field
        except Exception as err:
            messagebox.showerror("Database Error", str(err), parent=self.controller.root)
            self.controller.password_var.set("")  # Clear password field
