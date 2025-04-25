import math
import tkinter as tk
from Database import DatabaseManager as dbm
from PIL import ImageTk, Image
import io

# import the tk.Frame class that creates frames
class FindFrame(tk.Frame):
    frame_index = 5

    def __init__(self, master, controller):
        # initialise the imported class
        tk.Frame.__init__(self, master)

        # store an instance of controller in frame, easier to manage controller data
        self.controller = controller

        # self.local_conn = dbm.get_local_conn() # connect to local database
        # self.local_cursor = self.local_conn.cursor()  # create cursor to search through local database

        # connect to database and create cursor to traverse database
        self.rds_conn = dbm.get_rds_conn()
        self.rds_cursor = self.rds_conn.cursor()

        # retrieves battery serial number in database
        self.battery_info = None

        # creates label displaying serial number and places this label on the top-left part of screen
        self.serial_num = tk.Label(master=self)
        self.serial_num.grid(row=0, column=0)

        # creates label displaying part number and places this label on the top-centre part of screen
        self.part_num = tk.Label(master=self)
        self.part_num.grid(row=0, column=1)

        # creates label displaying item type and places this label on the centre-left part of screen
        self.item_type = tk.Label(master=self)
        self.item_type.grid(row=1, column=0)

        # creates label displaying battery description and places this label on the centre part of screen
        self.part_desc = tk.Label(master=self)
        self.part_desc.grid(row=1, column=1)

        # creates label displaying location together and places this label on the top-centre part of screen
        self.location = tk.Label(master=self)
        self.location.grid(row=0, column=2)

        # create button to go to the next page (report page), and places forward button at the bottom right of screen
        # when button is clicked, next page will be loaded
        self.forward_button = tk.Button(master=self)
        self.forward_button.config(width=20, text="Forward", command=lambda: self.complete_task())
        self.forward_button.grid(row=2, column=2, padx=10, pady=10, sticky="SE")

        # create button to go back to battery selection page, and places back button at the bottom left of screen
        # when button is clicked, previous page will be loaded
        self.back_button = tk.Button(master=self)
        self.back_button.config(width=20, text="Back", command=lambda: controller.back_button())
        self.back_button.grid(row=2, column=0, padx=10, pady=10, sticky="SW")

        """
        variable to manage images in database
        max_width and max_height help determine the aspect ratio based on the app's geometry
        image_tk is a tkinter handler for images
        image_label is a label to display image_tk
        """
        self.image = None
        self.max_width = math.floor(800 / 3)
        self.max_height = 480 / 3
        self.image_tk = None
        self.image_label = tk.Label(master=self)
        self.image_label.grid(row=1, column=2, padx=10, pady=10, sticky= "news")

    # search and display the relevant battery's information
    def find_item(self):
        # selects all batteries with the selected serial number
        self.rds_cursor.execute("""SELECT * FROM batteries where serial_number = ?""",
                                (self.controller.selected_battery_serial_number,))

        # stores the battery with this serial number, since all serial numbers are unique
        self.battery_info = self.rds_cursor.fetchall()

        # finds all location descriptions with the selected battery's location_id
        self.rds_cursor.execute("""SELECT location_description FROM locations where location_id = ?""",
                                (self.battery_info[0][4],))

        # stores the location with this location_id, since all serial numbers are unique
        location_desc = self.rds_cursor.fetchall()

        # displays the relevant variables in their respective tkinter Labels
        self.serial_num.config(text=f"Serial Number: {self.battery_info[0][0]}")
        self.part_num.config(text=f"Part Number: {self.battery_info[0][1]}")
        self.item_type.config(text=f"Item Type {self.battery_info[0][2]}")
        self.part_desc.config(text=f"Description: {self.battery_info[0][3]}")
        self.location.config(text = f"Location: {location_desc[0][0]}")

        # gets the picture of the selected battery
        self.rds_cursor.execute("""SELECT picture from batteries where serial_number = ?""", (self.battery_info[0][0],))
        result = self.rds_cursor.fetchall()

        # stores the photo from the database, as well as its width and height
        image_data = result[0][0]
        self.image = Image.open(io.BytesIO(image_data))
        og_width, og_height = self.image.size

        # Calculate the ratio to resize the image
        ratio = min(self.max_width / og_width, self.max_height / og_height)

        # If the image is bigger than the max dimensions (meaning the min ratio is less than 1), then resize
        if ratio < 1:
            new_width = int(og_width * ratio)
            new_height = int(og_height * ratio)
            self.image = self.image.resize((new_width, new_height), Image.LANCZOS)

        # process image with tkinter and display it in label
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.image_label.config(image=self.image_tk)

    # go to the emotion's page processor
    def complete_task(self):
        self.controller.show_page(-2)
        self.controller.frames[-2][1].update_emotion_list()


