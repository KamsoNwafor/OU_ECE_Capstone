import tkinter as tk
from tkinter import ttk

class ScanPage(tk.Frame):
    # Initialize the Barcode Entry Page
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#fafafa")
        self.controller = controller

        # Create header with title
        header = tk.Frame(self, bg="#4CAF50")
        header.pack(fill="x")
        tk.Label(header, text="Step 4: Enter Item Barcode", font=("Roboto", 14, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(pady=15)

        # Create content frame
        content = tk.Frame(self, bg="#f0f0f0", bd=1, relief="solid")
        content.pack(pady=10, padx=10, fill="both", expand=True)
        tk.Label(content, text="Enter the barcode:", font=("Roboto", 12, "bold"), bg="#f0f0f0", fg="#212121").pack(pady=10)

        # Barcode entry field
        self.barcode_entry = ttk.Entry(content, textvariable=self.controller.barcode_var, font=("Roboto", 11))
        self.barcode_entry.pack(pady=5, fill="x", padx=10)
        self.barcode_entry.focus_set()  # Set focus on barcode field
        # Bind Enter key to proceed
        self.barcode_entry.bind("<Return>", lambda e: self.controller.validate_and_proceed("ScanPage", "OperationSpecificPage", self.controller.barcode_var.get().strip(), "Barcode entry"))

        # Navigation buttons
        nav_frame = tk.Frame(content, bg="#f0f0f0")
        nav_frame.pack(pady=10)
        back_btn = ttk.Button(nav_frame, text="Back", style="Secondary.TButton", command=lambda: self.controller.go_back("ScanPage"))
        back_btn.pack(side="left", padx=5)
        next_btn = ttk.Button(nav_frame, text="Next", style="Primary.TButton", command=lambda: self.controller.validate_and_proceed("ScanPage", "OperationSpecificPage", self.controller.barcode_var.get().strip(), "Barcode entry"))
        next_btn.pack(side="left", padx=5)

    # Placeholder for camera stop (used in other pages)
    def stop_camera(self):
        pass
