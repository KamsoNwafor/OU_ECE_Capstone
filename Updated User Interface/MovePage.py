import tkinter as tk
from tkinter import ttk
from Database import DatabaseManager as dbm

# import the tk.Frame class that creates frames
class MoveFrame(tk.Frame):
    chosen_client = None
    frame_index = 7

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master, bg="#fafafa")  # Set soft background color

        self.controller = controller

        # connect to database and create cursor to traverse database
        self.rds_conn = dbm.get_rds_conn()
        self.rds_cursor = self.rds_conn.cursor()

        # create a null variable to store the locations
        self.locations = None

        # creates arrays to store the filtered locations in a drop down-list as well as their respective ids
        self.filtered_locations = []
        self.filtered_location_ids = []

        # create text entry variable and make it empty.
        self.location = tk.StringVar()
        self.location.set("")

        self.old_location = None

        # Create header with title
        header = tk.Frame(self, bg="#4CAF50")
        header.pack(fill="x")
        tk.Label(header, text="Step 5: Select New Location", font=("Roboto", 14, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(pady=15)

        # Create content frame
        content = tk.Frame(self, bg="#f0f0f0", bd=1, relief="solid")
        content.pack(pady=10, padx=10, fill="both", expand=True)

        # create label for current location
        self.old_location_label = tk.Label(content, font=("Roboto", 12, "bold"), bg="#f0f0f0", fg="#212121")
        self.old_location_label.grid(row=0, column=0, columnspan=2, pady=(10, 5))

        # create label for new location
        self.new_location = None
        self.new_location_label = tk.Label(content, text="SELECT NEW LOCATION", font=("Roboto", 11), bg="#f0f0f0", fg="#333333")
        self.new_location_label.grid(row=1, column=0, pady=5, sticky="w")

        # creates text entry bar for location, places text entry bar to the right of "location Name" label
        # sets the text in entry bar to be an entry variable, and filters the drop-down list everytime a key is pressed
        self.location_bar = ttk.Entry(content, textvariable=self.location)
        self.location_bar.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.location_bar.bind('<KeyRelease>', self.check_key)

        # creates scrollbar to manage there are many locations, puts scrollbar to the bottom-right of location text box
        self.location_scrollbar = ttk.Scrollbar(content, orient="vertical")
        self.location_scrollbar.grid(row=2, column=2, padx=(0, 10), pady=10, sticky="ns")

        # creates a box to show a filtered list of locations based on keyboard input, attaches list to scrollbar
        self.location_list = tk.Listbox(content, yscrollcommand=self.location_scrollbar.set, font=("Roboto", 11))
        self.location_list.grid(row=2, column=1, padx=(10, 0), pady=10, sticky="ew")

        # attaches scrollbar to list
        self.location_scrollbar.config(command=self.location_list.yview)

        # if a list item is double tapped, select it, place listbox to the left of scrollbar.
        # start with empty list
        self.location_list.bind("<Double-1>", self.location_selection)
        self.list_update(self.filtered_locations)

        # Navigation buttons
        nav_frame = tk.Frame(content, bg="#f0f0f0")
        nav_frame.grid(row=3, column=0, columnspan=3, pady=10)

        # button to go to the previous page (task selection page), places back button at the bottom left of screen
        self.back_button = ttk.Button(nav_frame, text="Back", style="Secondary.TButton", command=self.previous_page)
        self.back_button.pack(side="left", padx=5)

        # creates button to go to the next page (picture page), places forward button at the bottom right of screen
        # if a list item is highlighted, then the forward button is clicked, select it
        self.forward_button = ttk.Button(nav_frame, text="Forward", style="Primary.TButton", command=self.location_selection)
        self.forward_button.pack(side="left", padx=5)

    # filters the list based on current characters in text entry box.
    # If box is empty, empty the list (to reduce potential queries from the web)
    def check_key(self, event):
        # gets the text currently in the entry box
        value = event.widget.get()

        # if text is empty, empty the list
        if value == '':
            # keep location list empty if no key has been entered to save query costs
            # keep location id list empty if no key has been entered
            self.filtered_locations = []
            self.filtered_location_ids = []
        # if not, start with an empty array.
        # Then, add locations to the array if their ids contains the phrase in the entry box
        else:
            self.filtered_locations = []
            self.filtered_location_ids = []
            for item in self.locations:
                if value.lower() in item[1].lower():
                    self.filtered_locations.append(item[1])
                    self.filtered_location_ids.append(item[0])

        # update data in list with all the locations in the array
        self.list_update(self.filtered_locations)

    def list_update(self, data):
        # clear previous data
        self.location_list.delete(0, 'end')

        # put in new data, append each item in the list (insert each item at the end of the list)
        for item in data:
            self.location_list.insert('end', item)

    def location_selection(self, event=None):
        # makes sure a valid location was actually selected
        if self.filtered_locations and self.location_list.curselection():
            # returns the index of the item chosen as listed in the original list
            index = self.location_list.curselection()[0]

            # if a location in the list is selected, then update the text variable with the name selected
            for i in self.location_list.curselection():
                self.location.set(self.location_list.get(i))

            # Return the location of the given index (this accounts for duplicates)
            self.new_location = self.filtered_locations[index]
            self.controller.selected_location_id = self.filtered_location_ids[index]

            # go to the picture taking page
            self.controller.frames[8][1].image_preview()
            self.controller.show_page(8)

            # filters the list, so if location comes back from next page, they see only 1 item
            data = [self.new_location]
            self.list_update(data)

    def load_locations(self):
        self.rds_cursor.execute("SELECT * FROM locations")
        self.locations = self.rds_cursor.fetchall()

    def load_current_location(self):
        self.rds_cursor.execute("SELECT location FROM batteries WHERE serial_number = %s", (self.controller.selected_battery_serial_number,))
        result = self.rds_cursor.fetchall()

        if result:
            # self.old_location = result[0][0] if result else "Unknown", this messes up the method, so don't add it
            self.old_location = result[0][0]
            self.controller.old_location_id = self.old_location

            self.rds_cursor.execute("SELECT * FROM locations WHERE location_id = %s", (self.old_location,))
            result = self.rds_cursor.fetchall()

            self.old_location = result[0][1]
        else:
            self.old_location = "No Location"
        
        self.old_location_label.config (text =f"Current Location is: {self.old_location}")

    def previous_page(self):
        if self.controller.selected_task_id == "21":
            self.controller.show_page(9)
            self.controller.selected_battery_serial_number = None
            self.controller.selected_part_number = None
            self.controller.selected_item_type = None
            self.controller.input_battery_desc = None
        else:
            self.controller.show_page(4)
            self.controller.selected_battery_serial_number = None
            self.controller.old_location_id = None
