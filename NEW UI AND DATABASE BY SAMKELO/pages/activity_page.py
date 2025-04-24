import tkinter as tk
from tkinter import ttk

class ActivityPage(tk.Frame):
    # Initialize the Action Selection Page
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#fafafa")
        self.controller = controller

        # Create header with title
        header = tk.Frame(self, bg="#4CAF50")
        header.pack(fill="x")
        tk.Label(header, text="Step 3: Action", font=("Roboto", 14, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(pady=15)

        # Create content frame
        content = tk.Frame(self, bg="#f0f0f0", bd=1, relief="solid")
        content.pack(pady=10, padx=10, fill="both", expand=True)
        tk.Label(content, text="What are you doing?", font=("Roboto", 12, "bold"), bg="#f0f0f0", fg="#212121").pack(pady=10)
        # Action dropdown
        activity_dropdown = ttk.Combobox(content, textvariable=self.controller.action_var, values=["Find", "Receive", "Ship", "Move"], font=("Roboto", 11))
        activity_dropdown.pack(pady=5, fill="x", padx=10)

        # Navigation buttons
        nav_frame = tk.Frame(content, bg="#f0f0f0")
        nav_frame.pack(pady=10)
        back_btn = ttk.Button(nav_frame, text="Back", style="Secondary.TButton", command=lambda: self.controller.go_back("ActivityPage"))
        back_btn.pack(side="left", padx=5)
        next_btn = ttk.Button(nav_frame, text="Next", style="Primary.TButton", command=lambda: self.controller.validate_and_proceed("ActivityPage", "ScanPage", self.controller.action_var.get(), "Action selection"))
        next_btn.pack(side="left", padx=5)
