import tkinter as tk
from Database import DatabaseManager as dbm

# import the tk.Frame class that creates frames
class MoveFrame (tk.Frame):
    chosen_client = None
    frame_index = 6

    def __init__(self, master, controller):
        tk.Frame.__init__(self,master)

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
        self.old_location_label = tk.Label(master = self)
        self.old_location_label.grid(row = 0, column = 1)

        self.new_location = None
        self.new_location_label = tk.Label(master=self)
        self.new_location_label.config(text="SELECT NEW LOCATION")
        self.new_location_label.grid(row=1, column=0)

        # creates text entry bar for location, places text entry bar to the right of "location Name" label
        # sets the text in entry bar to be an entry variable, and filters the drop-down list everytime a key is pressed
        self.location_bar = tk.Entry(master=self)
        self.location_bar.grid(row=1, column=1)  #
        self.location_bar.config(textvariable=self.location)
        self.location_bar.bind('<KeyRelease>', self.check_key)

        # creates button to go to the next page (picture page), places forward button at the bottom right of screen
        # if a list item is highlighted, then the forward button is clicked, select it
        self.forward_button = tk.Button(master=self)
        self.forward_button.config(width=20, text="Forward")
        self.forward_button.grid(row=3, column=3, padx=10, pady=10, sticky="SE")
        self.forward_button.bind("<Button-1>", self.location_selection)

        # button to go to the previous page (task selection page), places back button at the bottom left of screen
        self.back_button = tk.Button(master=self)
        self.back_button.config(width=20, text="Back", command=lambda: self.previous_page())
        self.back_button.grid(row=3, column=0, padx=10, pady=10, sticky="SW")

        # creates scrollbar to manage there are many locations, puts scrollbar to the bottom-right of location text box
        self.location_scrollbar = tk.Scrollbar(master=self)
        self.location_scrollbar.grid(row=2, column=2, padx=10, pady=10, sticky="NS")

        # creates a box to show a filtered list of locations based on keyboard input, attaches list to scrollbar
        self.location_list = tk.Listbox(master=self)
        self.location_list.config(yscrollcommand=self.location_scrollbar.set)

        # attaches scrollbar to list
        self.location_scrollbar.config(command=self.location_list.yview)

        # if a list item is double tapped, select it, place listbox to the left of scrollbar.
        # start with empty list
        self.location_list.bind("<Double-1>", self.location_selection)
        self.location_list.grid(row=2, column=1, padx=10, pady=10)
        self.list_update(self.filtered_locations)

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

    def location_selection(self, event):
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
        self.rds_cursor.execute("""
        SELECT location
        FROM batteries
        WHERE serial_number = ?;
        """, (self.controller.selected_battery_serial_number,))

        result = self.rds_cursor.fetchall()

        self.old_location = result[0][0]
        self.controller.old_location_id = self.old_location

        self.rds_cursor.execute("""
                SELECT *
                FROM locations
                WHERE location_id = ?;
                """, (self.old_location,))
        
        result = self.rds_cursor.fetchall()

        if self.old_location:
            self.old_location = result[0][1]
        else:
            self.old_location = "No Location"
        
        self.old_location_label.config (text =f"Current Location is: {self.old_location}")

    def previous_page(self):
        self.controller.show_page(4)
        self.controller.selected_battery_serial_number = None
        self.controller.old_location_id = None
