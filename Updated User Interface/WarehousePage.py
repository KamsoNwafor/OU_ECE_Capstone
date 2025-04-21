import tkinter as tk
from Database import DatabaseManager as dbm

# import the tk.Frame class that creates frames
class WarehouseFrame(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)  # initialise the imported class

        # self.local_conn = dbm.get_local_conn() # connect to local database
        # self.local_cursor = self.local_conn.cursor() # create cursor to search through local database

        self.rds_conn = dbm.get_aws_conn() # connect to local database
        self.rds_cursor = self.rds_conn.cursor() # create cursor to search through local database

        self.rds_cursor.execute("select * from warehouses") # retrieves all data related to warehouse table in database
        self.warehouses = self.rds_cursor.fetchall() # retrieves warehouses in database

        self.filtered_warehouses = [] # creates array to store filtered warehouses in drop-down list
        self.filtered_warehouse_ids = [] # creates array to store filtered warehouse IDs

        self.controller = controller # store an instance of controller in frame, easier to manage controller data

        self.warehouse_label = tk.Label(master=self, text="Which Warehouse Is This?") # label asking for warehouse location
        self.warehouse_label.grid(row = 0, column = 1, padx = 10, pady = 10) # places this label at the top of screen in the centre

        self.location = tk.StringVar()  # variable to track text entry
        self.location.set("")  # set entry to be initially empty

        self.warehouse_input = tk.Entry(master=self) # create text entry box
        self.warehouse_input.config(textvariable=self.location) # assign entry to text variable string
        self.warehouse_input.grid(row=1, column=1, padx=10, pady=10) # places entry box below warehouse label
        self.warehouse_input.bind('<KeyRelease>', self.check_key) # filters list each time a key is pressed

        self.warehouse_scrollbar = tk.Scrollbar(master=self) # creates scrollbar
        self.warehouse_scrollbar.grid(row=2, column=2, padx=10, pady=10, sticky="NS") # places scrollbar to the bottom right of text entry, enlarges it if needed (does nothing if not)

        self.warehouse_list = tk.Listbox(master=self) # creates list
        self.warehouse_list.config(yscrollcommand = self.warehouse_scrollbar.set) # attaches scrollbar to list

        self.warehouse_scrollbar.config(command=self.warehouse_list.yview) # attaches list to scrollbar, now list will be directly under text entry box

        self.forward_button = tk.Button(master=self)  # button to go to the next page (password page)
        self.forward_button.config(width=20, text="Forward")
        self.forward_button.grid(row=3, column=3, padx=10, pady=10, sticky="SE")  # places forward button at the bottom right of screen

        self.forward_button.bind("<Button-1>", self.warehouse_selection)  # if a list item is highlighted, then the forward button is clicked, select it

        self.back_button = tk.Button(master=self) # creates a back button just in case the user wants to see my magnificent start screen
        self.back_button.config(width=20, text="Back", command = lambda: controller.back_button()) # makes button relatively wide (20% of screen), adds text "back" to it, and gives it the function to go to the previous frame
        self.back_button.grid(row = 3, column = 0, padx = 10, pady = 10, sticky="SW") # places back button at the bottom left of screen

        self.warehouse_list.bind("<Double-1>", self.warehouse_selection) # upon double-clicking an item in the list, selects the warehouse
        self.warehouse_list.grid(row=2, column=1, padx=10, pady=10)

        self.list_update(self.filtered_warehouses) # originally start with an empty list

    # filters the list based on current characters in text entry box. If box is empty, empty the list (to reduce potential queries from the web)
    def check_key(self, event):

        value = event.widget.get() # gets the text currently in the entry box

        # if text is empty, empty the list
        if value == '':
            self.filtered_warehouses = [] # keep warehouse list empty if no key has been entered to save query costs
            self.filtered_warehouse_ids = [] # keep warehouse id list empty if no key has been entered
        else: # if text is not empty
            self.filtered_warehouses = []
            self.filtered_warehouse_ids = []
            for item in self.warehouses: # start with an empty array, then add warehouses to the array if they contain the phrase in the entry box
                if value.lower() in item[1].lower():
                    self.filtered_warehouses.append(item[1])
                    self.filtered_warehouse_ids.append(item[0]) # track the warehouses and their ids, just in case the names have duplicates

        # update data in list with all the warehouses in the array
        self.list_update(self.filtered_warehouses)

    def list_update(self, data):
        # clear previous list
        self.warehouse_list.delete(0, 'end')

        # put in new data, append each item in the list (insert each item at the end of the list)
        for item in data:
            self.warehouse_list.insert('end', item)

    def warehouse_selection(self, event):
        index = self.warehouse_list.curselection()[0] # returns the index of the item chosen

        for i in self.warehouse_list.curselection(): # curselection is "cursor selection"
            self.location.set (self.warehouse_list.get(i)) # if a warehouse in the list is selected, then update the text variable with the name selected

        chosen_warehouse = self.filtered_warehouses[index]
        self.controller.selected_warehouse_id = self.filtered_warehouse_ids[index]  # Return the nth occurring warehouse selection (this accounts for duplicates)

        # Now update the UserFrame to reflect the selected warehouse
        self.controller.frames[2][1].update_warehouse() # updated the user page to see what warehouse they selected

        self.controller.frames[2][1].load_user_list()  # updated the list to show users that are in this warehouse

        self.controller.forward_button() # go to the next page (user page)

        data = [chosen_warehouse]
        self.list_update(data) # filters the list, so if user comes back from next page, they see only 1 item

