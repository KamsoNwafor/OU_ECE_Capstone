import tkinter as tk
from tkinter import ttk
from Database import DatabaseManager as dbm

class MoveFrame(tk.Frame):
    chosen_client = None
    frame_index = 7

    def __init__(self, master, controller):
        # Initialize frame with soft background
        tk.Frame.__init__(self, master, bg="#fafafa")
        self.controller = controller

        # Connect to RDS database
        self.rds_conn = dbm.get_rds_conn()
        self.rds_cursor = self.rds_conn.cursor()

        # Variables to manage locations
        self.locations = None
        self.filtered_locations = []
        self.filtered_location_ids = []
        self.location = tk.StringVar()
        self.old_location = None

        # Header
        header = tk.Frame(self, bg="#4CAF50")
        header.pack(fill="x")
        tk.Label(header, text="Step 5: Select New Location", font=("Roboto", 14, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(pady=8)

        # Main content
        content = tk.Frame(self, bg="#f0f0f0", bd=1, relief="solid")
        content.pack(padx=5, pady=5, fill="x", expand=False)

        # Configure grid layout
        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=2)
        content.grid_columnconfigure(2, weight=0)

        # Current location label
        self.old_location_label = tk.Label(content, font=("Roboto", 12, "bold"), bg="#f0f0f0", fg="#212121")
        self.old_location_label.grid(row=0, column=0, columnspan=2, pady=(5, 3), sticky="w")

        # New location label and entry
        self.new_location_label = tk.Label(content, text="SELECT NEW LOCATION", font=("Roboto", 11), bg="#f0f0f0", fg="#333333")
        self.new_location_label.grid(row=1, column=0, pady=(3, 3), padx=5, sticky="w")

        self.location_bar = ttk.Entry(content, textvariable=self.location)
        self.location_bar.grid(row=1, column=1, padx=5, pady=(3, 3), sticky="ew")
        self.location_bar.bind('<KeyRelease>', self.check_key)

        # Location listbox (shorter height) with scrollbar
        self.location_list = tk.Listbox(
            content,
            yscrollcommand=lambda *args: self.location_scrollbar.set(*args),
            font=("Roboto", 11),
            height=6  # Fixed height: 6 visible rows
        )
        self.location_list.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.location_list.bind("<Double-1>", self.location_selection)

        self.location_scrollbar = ttk.Scrollbar(content, orient="vertical", command=self.location_list.yview)
        self.location_scrollbar.grid(row=2, column=2, sticky="ns", pady=5, padx=(0, 5))

        self.list_update(self.filtered_locations)

        # Navigation buttons
        nav_frame = tk.Frame(content, bg="#f0f0f0")
        nav_frame.grid(row=3, column=0, columnspan=3, pady=(5, 5), sticky="ew")

        nav_frame.grid_columnconfigure(0, weight=1)
        nav_frame.grid_columnconfigure(1, weight=1)

        self.back_button = ttk.Button(nav_frame, text="Back", style="Secondary.TButton", command=self.previous_page)
        self.back_button.grid(row=0, column=0, padx=5)

        self.forward_button = ttk.Button(nav_frame, text="Forward", style="Primary.TButton", command=self.location_selection)
        self.forward_button.grid(row=0, column=1, padx=5)

    def check_key(self, event):
        # Filter locations based on current entry text
        value = event.widget.get()

        if value == '':
            self.filtered_locations = []
            self.filtered_location_ids = []
        else:
            self.filtered_locations = []
            self.filtered_location_ids = []
            for item in self.locations:
                if value.lower() in item[1].lower():
                    self.filtered_locations.append(item[1])
                    self.filtered_location_ids.append(item[0])

        self.list_update(self.filtered_locations)

    def list_update(self, data):
        # Update the listbox with filtered locations
        self.location_list.delete(0, 'end')
        for item in data:
            self.location_list.insert('end', item)

    def location_selection(self, event=None):
        # Select a location from the listbox
        if self.filtered_locations and self.location_list.curselection():
            index = self.location_list.curselection()[0]
            self.location.set(self.location_list.get(index))

            self.new_location = self.filtered_locations[index]
            self.controller.selected_location_id = self.filtered_location_ids[index]

            # Go to picture preview page
            self.controller.frames[8][1].image_preview()
            self.controller.show_page(8)

            # Lock the list to only the selected location afterward
            self.list_update([self.new_location])

    def load_locations(self):
        # Load all locations from database
        self.rds_cursor.execute("SELECT * FROM locations")
        self.locations = self.rds_cursor.fetchall()

    def load_current_location(self):
        # Load and display the current location of the selected battery
        self.rds_cursor.execute("SELECT location FROM batteries WHERE serial_number = %s", (self.controller.selected_battery_serial_number,))
        result = self.rds_cursor.fetchall()

        if result:
            self.old_location = result[0][0]
            self.controller.old_location_id = self.old_location

            self.rds_cursor.execute("SELECT * FROM locations WHERE location_id = %s", (self.old_location,))
            location_result = self.rds_cursor.fetchall()
            if location_result:
                self.old_location = location_result[0][1]
        else:
            self.old_location = "No Location"

        self.old_location_label.config(text=f"Current Location: {self.old_location}")

    def previous_page(self):
        # Go back depending on selected task
        self.controller.selected_battery_serial_number = None

        if self.controller.selected_task_id == "4":
            self.controller.show_page(4)
            self.controller.old_location_id = None
        else:
            self.controller.show_page(9)
            self.controller.selected_part_number = None
            self.controller.selected_item_type = None
            self.controller.input_battery_desc = None
