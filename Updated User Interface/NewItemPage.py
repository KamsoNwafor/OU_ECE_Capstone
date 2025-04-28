import tkinter as tk
from tkinter import ttk
from Database import DatabaseManager as dbm

class NewItemFrame(tk.Frame):
    chosen_client = None
    frame_index = 9

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master, bg="#fafafa")
        self.controller = controller

        # Connect to RDS database
        self.rds_conn = dbm.get_rds_conn()
        self.rds_cursor = self.rds_conn.cursor()

        # Form fields
        self.serial = tk.StringVar()
        self.part = tk.StringVar()
        self.item_type = tk.StringVar()
        self.desc = tk.StringVar()

        # Header
        header = tk.Frame(self, bg="#4CAF50")
        header.pack(fill="x")
        tk.Label(header, text="New Battery Details", font=("Roboto", 14, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(pady=10)

        # Content
        content = tk.Frame(self, bg="#f0f0f0", bd=1, relief="solid")
        content.pack(pady=5, padx=5, fill="x", expand=False)

        # Configure grid columns for even spacing
        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=1)
        content.grid_columnconfigure(2, weight=1)

        # Serial Number field
        self.serial_label = tk.Label(content, text="Battery Serial Number", font=("Roboto", 11), bg="#f0f0f0", fg="#333333")
        self.serial_label.grid(row=0, column=0, pady=(10, 5), padx=5, sticky="w")
        self.serial_entry = ttk.Entry(content, textvariable=self.serial)
        self.serial_entry.grid(row=1, column=0, pady=3, padx=5, sticky="ew")

        # Part Number field
        self.part_label = tk.Label(content, text="Battery Part Number", font=("Roboto", 11), bg="#f0f0f0", fg="#333333")
        self.part_label.grid(row=0, column=1, pady=(10, 5), padx=5, sticky="w")
        self.part_entry = ttk.Entry(content, textvariable=self.part)
        self.part_entry.grid(row=1, column=1, pady=3, padx=5, sticky="ew")

        # Item Type field
        self.item_type_label = tk.Label(content, text="Battery Item Type", font=("Roboto", 11), bg="#f0f0f0", fg="#333333")
        self.item_type_label.grid(row=0, column=2, pady=(10, 5), padx=5, sticky="w")
        self.item_type_entry = ttk.Entry(content, textvariable=self.item_type)
        self.item_type_entry.grid(row=1, column=2, pady=3, padx=5, sticky="ew")

        # Description field (spans all columns)
        self.desc_label = tk.Label(content, text="Battery Description", font=("Roboto", 11), bg="#f0f0f0", fg="#333333")
        self.desc_label.grid(row=2, column=0, columnspan=3, pady=(10, 5), padx=5, sticky="w")
        self.desc_entry = ttk.Entry(content, textvariable=self.desc)
        self.desc_entry.grid(row=3, column=0, columnspan=3, pady=3, padx=5, sticky="ew")

        # Navigation Buttons
        nav_frame = tk.Frame(content, bg="#f0f0f0")
        nav_frame.grid(row=4, column=0, columnspan=3, pady=10, sticky="ew")

        self.back_button = ttk.Button(nav_frame, text="Back", style="Secondary.TButton", command=self.previous_page)
        self.back_button.pack(side="left", padx=5)

        self.forward_button = ttk.Button(nav_frame, text="Forward", style="Primary.TButton", command=self.manage_details)
        self.forward_button.pack(side="left", padx=5)

    def previous_page(self):
        # Navigate back to Battery Selection
        self.controller.show_page(4)
        self.controller.selected_battery_serial_number = None

    def manage_details(self):
        # Validate form and store data
        if (self.serial.get() and self.part.get() and self.item_type.get() and self.desc.get()):
            self.controller.selected_battery_serial_number = self.serial.get()
            self.controller.selected_part_number = self.part.get()
            self.controller.selected_item_type = self.item_type.get()
            self.controller.input_battery_desc = self.desc.get()

            # Load move page
            self.controller.frames[7][1].load_locations()
            self.controller.frames[7][1].load_current_location()
            self.controller.show_page(7)

    def set_serial_num(self):
        # Set only the values, not textvariables again
        self.serial.set(self.controller.selected_battery_serial_number)
        self.part.set("")
        self.item_type.set("")
        self.desc.set("")
