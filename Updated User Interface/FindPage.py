import math
import tkinter as tk
from tkinter import ttk
from Database import DatabaseManager as dbm
from PIL import ImageTk, Image
import io

class FindFrame(tk.Frame):
    frame_index = 5

    def __init__(self, master, controller):
        # Initialize frame with soft background
        tk.Frame.__init__(self, master, bg="#fafafa")
        self.controller = controller

        # Connect to RDS database
        self.rds_conn = dbm.get_rds_conn()
        self.rds_cursor = self.rds_conn.cursor()

        # Variable to store retrieved battery info
        self.battery_info = None

        # Create header with page title
        header = tk.Frame(self, bg="#4CAF50")
        header.pack(fill="x")
        tk.Label(header, text="Find Item", font=("Roboto", 14, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(pady=10)

        # Create main content area
        content = tk.Frame(self, bg="#f0f0f0", bd=1, relief="solid")
        content.pack(pady=5, padx=5, fill="x", expand=False)

        # Configure grid layout: 3 balanced columns
        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=1)
        content.grid_columnconfigure(2, weight=1)

        # Create and place labels for battery information
        self.serial_num = tk.Label(content, font=("Roboto", 11), bg="#f0f0f0", fg="#333333")
        self.serial_num.grid(row=0, column=0, padx=5, pady=(5, 2), sticky="w")

        self.part_num = tk.Label(content, font=("Roboto", 11), bg="#f0f0f0", fg="#333333")
        self.part_num.grid(row=0, column=1, padx=5, pady=(5, 2))

        self.location = tk.Label(content, font=("Roboto", 11), bg="#f0f0f0", fg="#333333", anchor="center")
        self.location.grid(row=0, column=2, padx=(20, 5), pady=(5, 2), sticky="w")

        self.item_type = tk.Label(content, font=("Roboto", 11), bg="#f0f0f0", fg="#333333")
        self.item_type.grid(row=1, column=0, padx=5, pady=2, sticky="w")

        self.part_desc = tk.Label(content, font=("Roboto", 11), bg="#f0f0f0", fg="#333333")
        self.part_desc.grid(row=1, column=1, padx=5, pady=2)

        # Setup image display
        self.image = None
        self.max_width = math.floor(800 / 2.5)
        self.max_height = 480 / 2.5
        self.image_tk = None
        self.image_label = tk.Label(content, bg="#f0f0f0")
        self.image_label.grid(row=1, column=2, padx=5, pady=5, sticky="news")

        # Navigation buttons (Back and Forward)
        nav_frame = tk.Frame(content, bg="#f0f0f0")
        nav_frame.grid(row=2, column=0, columnspan=3, pady=(10, 5))

        self.back_button = ttk.Button(nav_frame, text="Back", style="Secondary.TButton", command=self.previous_page)
        self.back_button.pack(side="left", padx=5)

        self.forward_button = ttk.Button(nav_frame, text="Forward", style="Primary.TButton", command=self.complete_task)
        self.forward_button.pack(side="left", padx=5)

    def find_item(self):
        # Fetch battery info from database
        self.rds_cursor.execute("SELECT * FROM batteries WHERE serial_number = %s", (self.controller.selected_battery_serial_number,))
        self.battery_info = self.rds_cursor.fetchall()

        # Fetch battery's location description
        self.rds_cursor.execute("SELECT location_description FROM locations WHERE location_id = %s", (self.battery_info[0][4],))
        location_desc = self.rds_cursor.fetchall()

        # Update text labels with retrieved battery info
        if self.battery_info:
            self.serial_num.config(text=f"Serial Number: {self.battery_info[0][0] or 'N/A'}")
            self.part_num.config(text=f"Part Number: {self.battery_info[0][1] or 'N/A'}")
            self.item_type.config(text=f"Item Type: {self.battery_info[0][2] or 'N/A'}")
            self.part_desc.config(text=f"Description: {self.battery_info[0][3] or 'N/A'}")
        else:
            self.serial_num.config(text="Serial Number: Not found")
            self.part_num.config(text="Part Number: Not found")
            self.item_type.config(text="Item Type: Not found")
            self.part_desc.config(text="Description: Not found")

        # Update location
        if location_desc:
            self.location.config(text=f"Location: {location_desc[0][0]}")
        else:
            self.location.config(text="Location: Not found")

        # Load and display battery image
        self.rds_cursor.execute("SELECT picture FROM batteries WHERE serial_number = %s", (self.battery_info[0][0],))
        result = self.rds_cursor.fetchall()

        if result and result[0][0]:
            try:
                image_data = result[0][0]
                self.image = Image.open(io.BytesIO(image_data))
                og_width, og_height = self.image.size

                # Calculate resize ratio
                ratio = min(self.max_width / og_width, self.max_height / og_height)

                if ratio < 1:
                    new_width = int(og_width * ratio)
                    new_height = int(og_height * ratio)
                    self.image = self.image.resize((new_width, new_height), Image.Resampling.LANCZOS)

                self.image_tk = ImageTk.PhotoImage(self.image)
                self.image_label.config(image=self.image_tk, text="")
            except Exception as e:
                self.image_label.config(image="", text=f"Error loading image: {str(e)}")
        else:
            self.image_label.config(image="", text="No image available")

    def complete_task(self):
        # Move to Emotion Selection page
        self.controller.frames[-2][1].update_emotion_list()
        self.controller.show_page(-2)

    def previous_page(self):
        # Return to battery selection page
        self.controller.show_page(4)
        self.controller.selected_battery_serial_number = None
