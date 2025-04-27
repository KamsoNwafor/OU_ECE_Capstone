


import math
import tkinter as tk
from tkinter import ttk
from Database import DatabaseManager as dbm
from PIL import ImageTk, Image
import io

# import the tk.Frame class that creates frames
class FindFrame(tk.Frame):
    frame_index = 5

    def __init__(self, master, controller):
        # initialise the imported class
        tk.Frame.__init__(self, master, bg="#fafafa")  # Set soft background color

        # store an instance of controller in frame, easier to manage controller data
        self.controller = controller

        # self.local_conn = dbm.get_local_conn() # connect to local database
        # self.local_cursor = self.local_conn.cursor()  # create cursor to search through local database

        # connect to database and create cursor to traverse database
        self.rds_conn = dbm.get_rds_conn()
        self.rds_cursor = self.rds_conn.cursor()

        # retrieves battery serial number in database
        self.battery_info = None

        # Create header with title
        header = tk.Frame(self, bg="#4CAF50")
        header.pack(fill="x")
        tk.Label(header, text="Step 5: Find Item", font=("Roboto", 14, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(pady=15)

        # Create content frame
        content = tk.Frame(self, bg="#f0f0f0", bd=1, relief="solid")
        content.pack(pady=10, padx=10, fill="both", expand=True)

        # creates label displaying serial number and places this label on the top-left part of screen
        self.serial_num = tk.Label(content, font=("Roboto", 11), bg="#f0f0f0", fg="#333333")
        self.serial_num.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # creates label displaying part number and places this label on the top-centre part of screen
        self.part_num = tk.Label(content, font=("Roboto", 11), bg="#f0f0f0", fg="#333333")
        self.part_num.grid(row=0, column=1, padx=5, pady=5)

        # creates label displaying location together and places this label on the top-right part of screen
        self.location = tk.Label(content, font=("Roboto", 11), bg="#f0f0f0", fg="#333333")
        self.location.grid(row=0, column=2, padx=5, pady=5, sticky="e")

        # creates label displaying item type and places this label on the centre-left part of screen
        self.item_type = tk.Label(content, font=("Roboto", 11), bg="#f0f0f0", fg="#333333")
        self.item_type.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        # creates label displaying battery description and places this label on the centre part of screen
        self.part_desc = tk.Label(content, font=("Roboto", 11), bg="#f0f0f0", fg="#333333")
        self.part_desc.grid(row=1, column=1, padx=5, pady=5)

        """
        variable to manage images in database
        max_width and max_height help determine the aspect ratio based on the app's geometry
        image_tk is a tkinter handler for images
        image_label is a label to display image_tk
        """
        self.image = None
        self.max_width = math.floor(800 / 2)
        self.max_height = 480 / 2
        self.image_tk = None
        self.image_label = tk.Label(content, bg="#f0f0f0")
        self.image_label.grid(row=1, column=2, padx=10, pady=10, sticky="news")

        # Navigation buttons
        nav_frame = tk.Frame(content, bg="#f0f0f0")
        nav_frame.grid(row=2, column=0, columnspan=3, pady=10)

        # create button to go back to battery selection page, and places back button at the bottom left of screen
        # when button is clicked, previous page will be loaded
        self.back_button = ttk.Button(nav_frame, text="Back", style="Secondary.TButton", command=self.previous_page)
        self.back_button.pack(side="left", padx=5)

        # create button to go to the next page (report page), and places forward button at the bottom right of screen
        # when button is clicked, next page will be loaded
        self.forward_button = ttk.Button(nav_frame, text="Forward", style="Primary.TButton", command=self.complete_task)
        self.forward_button.pack(side="left", padx=5)

    # search and display the relevant battery's information
    def find_item(self):
        # selects all batteries with the selected serial number
        self.rds_cursor.execute("SELECT * FROM batteries WHERE serial_number = %s",
                                (self.controller.selected_battery_serial_number,))
        # stores the battery with this serial number, since all serial numbers are unique
        self.battery_info = self.rds_cursor.fetchall()

        # finds all location descriptions with the selected battery's location_id
        self.rds_cursor.execute("SELECT location_description FROM locations WHERE location_id = %s",
                                (self.battery_info[0][4],))
        # stores the location with this location_id, since all serial numbers are unique
        location_desc = self.rds_cursor.fetchall()

        # Handle cases where data might be missing
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

        if location_desc:
            self.location.config(text=f"Location: {location_desc[0][0]}")
        else:
            self.location.config(text="Location: Not found")

        # gets the picture of the selected battery
        self.rds_cursor.execute("SELECT picture FROM batteries WHERE serial_number = %s", (self.battery_info[0][0],))
        result = self.rds_cursor.fetchall()

        # Handle image loading
        if result and result[0][0]:
            try:
                image_data = result[0][0]
                self.image = Image.open(io.BytesIO(image_data))
                og_width, og_height = self.image.size

                # It seemed I swapped the dividend and divisor. og should be divided by max, then max multiplied by the quotient
                # Calculate the ratio to resize the image
                ratio = min(self.max_width / og_width, self.max_height / og_height)

                # If the image is bigger than the max dimensions (meaning the min ratio is less than 1), then resize
                if ratio < 1:
                    new_width = int(og_width * ratio)
                    new_height = int(og_height * ratio)
                    self.image = self.image.resize((new_width, new_height), Image.Resampling.LANCZOS)

                # process image with tkinter and display it in label
                self.image_tk = ImageTk.PhotoImage(self.image)
                self.image_label.config(image=self.image_tk)
            except Exception as e:
                self.image_label.config(image="", text=f"Error loading image: {str(e)}")
        else:
            self.image_label.config(image="", text="No image available")

    # go to the emotion's page processor
    def complete_task(self):
        self.controller.frames[-2][1].update_emotion_list()
        self.controller.show_page(-2)

    def previous_page(self):
        self.controller.show_page(4)
        self.controller.selected_battery_serial_number = None
