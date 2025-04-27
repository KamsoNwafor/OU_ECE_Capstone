import tkinter as tk
from tkinter import ttk
from Database import DatabaseManager as dbm

class NewItemFrame(tk.Frame):
    chosen_client = None
    frame_index = 9

    def __init__(self, master, controller):
        # Initialize the frame with a light gray background
        tk.Frame.__init__(self, master, bg="#fafafa")
        self.controller = controller

        # Connect to the RDS database
        self.rds_conn = dbm.get_rds_conn()
        # Create a cursor to execute queries on the RDS database
        self.rds_cursor = self.rds_conn.cursor()

        # I had to initialise them in set_serial_num or they messed up the report_page

        # Initialize string variables for form inputs
        self.serial = None
        self.part = None
        self.item_type = None
        self.desc = None

        # Create header frame with a green background and title
        header = tk.Frame(self, bg="#4CAF50")
        header.pack(fill="x")
        tk.Label(header, text="Step 4: New Battery Details", font=("Roboto", 14, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(pady=15)

        # Create content frame with a subtle border and light gray background
        content = tk.Frame(self, bg="#f0f0f0", bd=1, relief="solid")
        content.pack(pady=10, padx=10, fill="both", expand=True)

        # Serial number label
        self.serial_label = tk.Label(content, text="Battery Serial Number", font=("Roboto", 11), bg="#f0f0f0", fg="#333333")
        self.serial_label.grid(row=0, column=0, pady=(10, 5), padx=10, sticky="w")

        # Sorry for this, I needed initialise serial only when a function was called,
        # so I had to configure all the entries
        # All configs to set textvariables can be found in set_serial_num

        # Serial number entry
        self.serial_entry = ttk.Entry(content)
        self.serial_entry.grid(row=1, column=0, pady=5, padx=10, sticky="w")

        # Part number label
        self.part_label = tk.Label(content, text="Battery Part Number", font=("Roboto", 11), bg="#f0f0f0", fg="#333333")
        self.part_label.grid(row=0, column=1, pady=(10, 5), padx=10, sticky="w")

        # Part number entry
        self.part_entry = ttk.Entry(content)
        self.part_entry.grid(row=1, column=1, pady=5, padx=10, sticky="w")

        # Item type label
        self.item_type_label = tk.Label(content, text="Battery Item Type", font=("Roboto", 11), bg="#f0f0f0", fg="#333333")
        self.item_type_label.grid(row=0, column=2, pady=(10, 5), padx=10, sticky="w")

        # Item type entry
        self.item_type_entry = ttk.Entry(content)
        self.item_type_entry.grid(row=1, column=2, pady=5, padx=10, sticky="w")

        # Description label
        self.desc_label = tk.Label(content, text="Battery Description", font=("Roboto", 11), bg="#f0f0f0", fg="#333333")
        self.desc_label.grid(row=2, column=0, pady=(10, 5), padx=10, sticky="w")

        # Description entry (wider to accommodate longer text)
        self.desc_entry = ttk.Entry(content)
        self.desc_entry.grid(row=3, column=0, columnspan=3, pady=5, padx=10, sticky="ew")

        # Navigation buttons frame
        nav_frame = tk.Frame(content, bg="#f0f0f0")
        nav_frame.grid(row=4, column=0, columnspan=3, pady=20, sticky="ew")

        # Back button to return to the previous page
        self.back_button = ttk.Button(nav_frame, text="Back", style="Secondary.TButton", command=self.previous_page)
        self.back_button.pack(side="left", padx=5)

        # Forward button to submit details and proceed
        self.forward_button = ttk.Button(nav_frame, text="Forward", style="Primary.TButton", command=self.manage_details)
        self.forward_button.pack(side="left", padx=5)

    def previous_page(self):
        # Navigate back to the battery selection page (index 4)
        self.controller.show_page(4)
        # Clear the input battery description in the controller
        self.controller.selected_battery_serial_number = None
        # Reset all fields
        self.serial = None
        self.part = None
        self.item_type = None
        self.desc = None

    def manage_details(self):
        # Check if all fields are filled
        if (self.serial.get() != "" and self.part.get() != "" and 
            self.item_type.get() != "" and self.desc.get() != ""):
            # Store form data in the controller
            self.controller.selected_battery_serial_number = self.serial.get()
            self.controller.selected_part_number = self.part.get()
            self.controller.selected_item_type = self.item_type.get()
            self.controller.input_battery_desc = self.desc.get()

            # Prepare Move Page to set location
            self.controller.frames[7][1].load_locations()
            self.controller.frames[7][1].load_current_location()
            # Navigate to Move Page
            self.controller.show_page(7)

    def set_serial_num(self):

        # Initialize string variables for form inputs
        self.serial = tk.StringVar()
        self.serial.set("")
        self.part = tk.StringVar()
        self.part.set("")
        self.item_type = tk.StringVar()
        self.item_type.set("")
        self.desc = tk.StringVar()
        self.desc.set("")

        self.serial_entry.config(textvariable=self.serial)
        self.part_entry.config(textvariable=self.part)
        self.item_type_entry.config(textvariable=self.item_type)
        self.desc_entry.config(textvariable=self.desc)

        # Set the description field to the input battery description from the controller
        self.serial.set(self.controller.selected_battery_serial_number)
