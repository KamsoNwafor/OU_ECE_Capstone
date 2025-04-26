import tkinter as tk
from Database import DatabaseManager as dbm

# import the tk.Frame class that creates frames
class ItemSelectionFrame(tk.Frame):
    chosen_battery = None
    frame_index = 4

    def __init__(self, master, controller):
        # initialise the imported class
        tk.Frame.__init__(self, master)

        # store an instance of controller in frame, easier to manage controller data
        self.controller = controller

        # self.local_conn = dbm.get_local_conn()  # connect to local database
        # self.local_cursor = self.local_conn.cursor()  # create cursor to search through local database

        # connect to local database
        self.rds_conn = dbm.get_rds_conn()
        # create cursor to traverse local database
        self.rds_cursor = self.rds_conn.cursor()

        # create a null variable to store the batteries
        self.batteries = None

        # creates arrays to store the filtered batteries in a drop down-list as well as their respective serial numbers
        self.filtered_batteries = []
        self.filtered_battery_ids = []

        # store selected user from previous page and display selected user on top centre side of screen
        self.user_name = tk.Label(master=self)
        self.user_name.grid(row=0, column=1)

        # create text entry variable and make it empty.
        self.battery = tk.StringVar()
        self.battery.set("")

        # creates a label asking for the battery name and places this label in the centre-left part of screen
        self.battery_name = tk.Label(master=self)
        self.battery_name.config(text="Enter Battery Here, or Scan Barcode")
        self.battery_name.grid(row=1, column=0)

        # creates text entry bar for battery, places text entry bar to the right of "Battery Name" label
        # sets the text in entry bar to be an entry variable, and filters the drop-down list everytime a key is pressed
        self.battery_bar = tk.Entry(master=self)
        self.battery_bar.grid(row=1, column=1)  #
        self.battery_bar.config(textvariable=self.battery)
        self.battery_bar.bind('<KeyRelease>', self.check_key)

        # creates button to go to the next page (selected task), places forward button at the bottom right of screen
        # if a list item is highlighted, then the forward button is clicked, select it
        self.forward_button = tk.Button(master=self)
        self.forward_button.config(width=20, text="Forward")
        self.forward_button.grid(row=3, column=3, padx=10, pady=10, sticky="SE")
        self.forward_button.bind("<Button-1>", self.battery_selection)

        # button to go to the previous page (task selection page), places back button at the bottom left of screen
        self.back_button = tk.Button(master=self)
        self.back_button.config(width=20, text="Back", command=lambda: controller.back_button())
        self.back_button.grid(row=3, column=0, padx=10, pady=10, sticky="SW")

        # creates scrollbar to manage there are many batteries, puts scrollbar to the bottom-right of battery text box
        self.battery_scrollbar = tk.Scrollbar(master=self)
        self.battery_scrollbar.grid(row=2, column=2, padx=10, pady=10, sticky="NS")

        # creates a box to show a filtered list of batteries based on keyboard input, attaches list to scrollbar
        self.battery_list = tk.Listbox(master=self)
        self.battery_list.config(yscrollcommand=self.battery_scrollbar.set)

        # attaches scrollbar to list
        self.battery_scrollbar.config(command=self.battery_list.yview)

        # if a list item is double tapped, select it, place listbox to the left of scrollbar.
        # start with empty list
        self.battery_list.bind("<Double-1>", self.battery_selection)
        self.battery_list.grid(row=2, column=1, padx=10, pady=10)
        self.list_update(self.filtered_batteries)

    # filters the list based on current characters in text entry box.
    # If box is empty, empty the list (to reduce potential queries from the web)
    def check_key(self, event):
        # gets the text currently in the entry box
        value = event.widget.get()

        # if text is empty, empty the list
        if value == '':
            # keep battery list empty if no key has been entered to save query costs
            # keep battery id list empty if no key has been entered
            self.filtered_batteries = []
            self.filtered_battery_ids = []
        # if not, start with an empty array.
        # Then, add batteries to the array if their serial number contains the phrase in the entry box
        else:
            self.filtered_batteries = []
            self.filtered_battery_ids = []
            for item in self.batteries:
                if value.lower() in item[1].lower():
                    self.filtered_batteries.append(item[1])
                    self.filtered_battery_ids.append(item[0])

        # update data in list with all the batteries in the array
        self.list_update(self.filtered_batteries)

    def list_update(self, data):
        # clear previous data
        self.battery_list.delete(0, 'end')

        # put in new data, append each item in the list (insert each item at the end of the list)
        for item in data:
            self.battery_list.insert('end', item)

    def update_user(self):
        # self.local_cursor.execute("""select first_name, last_name, warehouse_id from employees where user_id = ?""", (self.controller.selected_user_id,))
        # result = self.local_cursor.fetchall()

        # gets the first name and last name of the previously saved user_id and saves the results
        self.rds_cursor.execute("select first_name, last_name from employees where user_id = ?", (self.controller.selected_user_id,))
        result = self.rds_cursor.fetchall()

        # combines the employee names, and display this username on the screen
        employee_name = f"{result[0][0]} {result[0][1]}"
        self.user_name.config(text="Selected User Name: " + employee_name)

    def battery_selection(self, event):
        # returns the index of the item chosen as listed in the original list
        index = self.battery_list.curselection()[0]

        # if a battery in the list is selected, then update the text variable with the name selected
        for i in self.battery_list.curselection():
            self.battery.set(self.battery_list.get(i))

        # Return the battery of the given index (this accounts for duplicates)
        self.chosen_battery = self.filtered_batteries[index]
        self.controller.selected_battery_serial_number = self.filtered_battery_ids[index]

        # show the page for the corresponding task selected on the previous page
        self.show_task_page()

        # filters the list, so if battery comes back from next page, they see only 1 item
        data = [self.chosen_battery]
        self.list_update(data)

    def show_task_page (self):
        # if find is selected, show find page
        if self.controller.selected_task_id == "1":
            self.controller.frames[5][1].find_item()
            self.controller.show_page(5)
        # if receive or ship is selected, show receive/ship page
        elif (self.controller.selected_task_id == "2"
           or self.controller.selected_task_id == "3"):
            self.controller.frames[6][1].update_client_task_list()
            self.controller.show_page(6)
        # if move is selected, show move page
        elif self.controller.selected_task_id == "4":
            self.controller.show_page(7)
        # if take picture is selected, show take picture page
        elif self.controller.selected_task_id == "20":
            self.controller.frames[8][1].image_preview()
            self.controller.show_page(8)
        # if intake new item is selected, show update battery status page
        elif self.controller.selected_task_id == "21":
            self.controller.show_page(9)

    def load_battery_list(self):
        # finds all battery serial numbers in database and saves them as the original list of batteries
        self.rds_cursor.execute("select serial_number, part_description from batteries")
        self.batteries = self.rds_cursor.fetchall()

    def previous_page(self):
        self.controller.show_page(3)
        self.controller.selected_task_id = None