import tkinter as tk
from Database import DatabaseData

# import the tk.Frame class that creates frames
class WarehouseFrame(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)  # initialise the imported class

        warehouse_data = DatabaseData()
        self.warehouses = warehouse_data.get_warehouses() # store an instance of the data in the warehouse page

        self.controller = controller # store an instance of controller in frame, easier to manage controller data

        self.warehouse_label = tk.Label(master=self, text="Which Warehouse Is This?") # label asking for warehouse location
        self.warehouse_label.grid (row = 0, column = 1, padx = 10, pady = 10) # places warehouse at the top of screen in the centre

        self.location = tk.StringVar() # variable to track text entry
        self.location.set("") # set entry to be initially empty

        self.warehouse_input = tk.Entry(master=self) # create text entry box
        self.warehouse_input.config(textvariable=self.location) # assign entry to text variable string
        self.warehouse_input.grid(row=1, column=1, padx=10, pady=10) # places entry box below warehouse label
        self.warehouse_input.bind('<KeyRelease>', self.check_key) # filters list each time a key is pressed

        self.warehouse_scrollbar = tk.Scrollbar(master=self) # creates scrollbar
        self.warehouse_scrollbar.grid(row=2, column=2, padx=10, pady=10, sticky="NEWS") # places scrollbar to the bottom right of text entry, enlarges it if needed (does nothing if not)

        self.warehouse_list = tk.Listbox(master=self) # creates list
        self.warehouse_list.config(yscrollcommand = self.warehouse_scrollbar.set) # attaches scrollbar to list

        self.warehouse_scrollbar.config(command=self.warehouse_list.yview) # attaches list to scrollbar, now list will be directly under text entry box

        self.back_button = tk.Button(master=self) # creates a back button just in case the user wants to see my magnificent start screen
        self.back_button.config(width=20, text="Back", command = lambda: controller.back_button()) # makes button relatively wide (20% of screen), adds text "back" to it, and gives it the function to go to the previous frame
        self.back_button.grid(row = 3, column = 0, padx = 10, pady = 10, sticky="SW")

        self.warehouse_list.bind("<Double-1>", self.warehouse_selection) # upon double-clicking an item in the list, selects the warehouse
        self.warehouse_list.grid(row=2, column=1, padx=10, pady=10)
        self.list_update([])

    def check_key(self, event): # filters the list based on current characters in text entry box. If box is empty, empty the list (to reduce potential queries from the web)
        value = event.widget.get() # gets the text currently in the entry box

        # if text is empty, empty the list
        if value == '':
            data = []
        else: # if text is not empty
            data = []
            for item in self.warehouses: # start with an empty array, then add warehouses to the array if they contain the phrase in the entry box
                if value.lower() in item.lower():
                    data.append(item)

        # update data in list with all the warehouses in the array
        self.list_update(data)

    def list_update(self, data):
        # clear previous list
        self.warehouse_list.delete(0, 'end')

        # put in new data, append each item in the list (insert each item at the end of the list)
        for item in data:
            self.warehouse_list.insert('end', item)

    def warehouse_selection(self, event):
        for i in self.warehouse_list.curselection(): # curselection is "cursor selection"
            self.location.set (self.warehouse_list.get(i)) # if a warehouse in the list is selected, then updated the text variable with the name of the list

        self.controller.selected_warehouse = self.location.get() # updated the app's warehouse with the text variable

        # Now update the UserFrame to reflect the selected warehouse
        self.controller.frames[2][1].update_warehouse() # updated the user page to see what warehouse they selected

        self.controller.forward_button() # go to the next page (user page)

        data = [self.controller.selected_warehouse]
        self.list_update(data) # filters the list, so if user comes back from next page, they see only 1 item

