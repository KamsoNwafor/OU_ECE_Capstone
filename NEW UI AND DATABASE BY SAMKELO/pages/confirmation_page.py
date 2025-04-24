import tkinter as tk
from tkinter import ttk

class ConfirmationPage(tk.Frame):
    # Initialize the Confirmation Page
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#fafafa")
        self.controller = controller

        # Create header with title
        header = tk.Frame(self, bg="#4CAF50")
        header.pack(fill="x")
        tk.Label(header, text="Step 8: Confirm Details", font=("Roboto", 14, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(pady=15)

        # Create content frame
        content = tk.Frame(self, bg="#f0f0f0", bd=1, relief="solid")
        content.pack(pady=10, padx=10, fill="both", expand=True)
        tk.Label(content, text="Review your submission:", font=("Roboto", 12, "bold"), bg="#f0f0f0", fg="#212121").pack(pady=10)

        # Display technician ID
        tk.Label(content, text="Technician ID:", font=("Roboto", 11, "bold"), bg="#f0f0f0", fg="#212121", anchor="w").pack(fill="x", padx=10)
        tk.Label(content, text=self.controller.user_id_var.get() or "N/A", font=("Roboto", 11), bg="#f0f0f0", fg="#333333", anchor="w").pack(fill="x", padx=10)

        # Display location
        tk.Label(content, text="Location:", font=("Roboto", 11, "bold"), bg="#f0f0f0", fg="#212121", anchor="w").pack(fill="x", padx=10)
        tk.Label(content, text=self.controller.location_var.get() or "N/A", font=("Roboto", 11), bg="#f0f0f0", fg="#333333", anchor="w").pack(fill="x", padx=10)

        # Display action
        tk.Label(content, text="Action:", font=("Roboto", 11, "bold"), bg="#f0f0f0", fg="#212121", anchor="w").pack(fill="x", padx=10)
        tk.Label(content, text=self.controller.action_var.get() or "N/A", font=("Roboto", 11), bg="#f0f0f0", fg="#333333", anchor="w").pack(fill="x", padx=10)

        # Display barcode
        tk.Label(content, text="Barcode:", font=("Roboto", 11, "bold"), bg="#f0f0f0", fg="#212121", anchor="w").pack(fill="x", padx=10)
        tk.Label(content, text=self.controller.barcode_var.get() or "N/A", font=("Roboto", 11), bg="#f0f0f0", fg="#333333", anchor="w").pack(fill="x", padx=10)

        # Display operation-specific fields
        operation = self.controller.action_var.get().strip()
        if operation in self.controller.OPERATION_TEMPLATES and self.controller.OPERATION_TEMPLATES[operation]["fields"]:
            for field in self.controller.OPERATION_TEMPLATES[operation]["fields"]:
                if field.get("lookup"):
                    continue  # Skip lookup fields
                tk.Label(content, text=field["label"], font=("Roboto", 11, "bold"), bg="#f0f0f0", fg="#212121", anchor="w").pack(fill="x", padx=10)
                # Retrieve field value based on variable name
                if field["variable"] == "new_location_var":
                    value = self.controller.new_location_var.get()
                elif field["variable"] == "battery_condition_var":
                    value = self.controller.battery_condition_var.get()
                elif field["variable"] == "destination_var":
                    value = self.controller.destination_var.get()
                elif field["variable"] == "source_var":
                    value = self.controller.source_var.get()
                else:
                    value = "N/A"
                tk.Label(content, text=value or "N/A", font=("Roboto", 11), bg="#f0f0f0", fg="#333333", anchor="w").pack(fill="x", padx=10)

        # Display battery condition for customer source
        if operation == "Receive" and self.controller.source_var.get() == "Customer":
            tk.Label(content, text="Battery Condition:", font=("Roboto", 11, "bold"), bg="#f0f0f0", fg="#212121", anchor="w").pack(fill="x", padx=10)
            tk.Label(content, text=self.controller.customer_battery_condition_var.get() or "N/A", font=("Roboto", 11), bg="#f0f0f0", fg="#333333", anchor="w").pack(fill="x", padx=10)

        # Display photo path
        tk.Label(content, text="Photo Path:", font=("Roboto", 11, "bold"), bg="#f0f0f0", fg="#212121", anchor="w").pack(fill="x", padx=10)
        photo_path = self.controller.frames["PhotoPage"].photo_path if self.controller.frames["PhotoPage"].photo_path else "N/A"
        tk.Label(content, text=photo_path, font=("Roboto", 11), bg="#f0f0f0", fg="#333333", anchor="w").pack(fill="x", padx=10)

        # Display reaction sentence
        tk.Label(content, text="Reaction:", font=("Roboto", 11, "bold"), bg="#f0f0f0", fg="#212121", anchor="w").pack(fill="x", padx=10)
        reaction = f"I feel {self.controller.adjective_var.get()} about {self.controller.action_var.get()} because it’s {self.controller.reason_var.get()}." if self.controller.adjective_var.get() and self.controller.reason_var.get() else "N/A"
        tk.Label(content, text=reaction, font=("Roboto", 11), bg="#f0f0f0", fg="#666666", anchor="w", wraplength=700).pack(fill="x", padx=10)

        # Navigation buttons
        nav_frame = tk.Frame(content, bg="#f0f0f0")
        nav_frame.pack(pady=10)
        back_btn = ttk.Button(nav_frame, text="Back", style="Secondary.TButton", command=lambda: self.controller.go_back("ConfirmationPage"))
        back_btn.pack(side="left", padx=5)
        next_btn = ttk.Button(nav_frame, text="Next", style="Primary.TButton", command=lambda: self.controller.show_frame("DonePage"))
        next_btn.pack(side="left", padx=5)
