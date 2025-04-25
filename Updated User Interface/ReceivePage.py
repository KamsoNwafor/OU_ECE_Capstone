import tkinter as tk
from Database import DatabaseManager as dbm

# import the tk.Frame class that creates frames
class ReceiveFrame (tk.Frame):
    chosen_supplier = None
    frame_index = 6

    def __init__(self, master, controller):
        # initialise the imported class
        tk.Frame.__init__(self, master)

        # store an instance of controller in frame, easier to manage controller data
        self.controller = controller

        # self.local_conn = dbm.get_local_conn()  # connect to database
        # self.local_cursor = self.local_conn.cursor()  # create cursor to traverse database

        # connect to local database
        self.rds_conn = dbm.get_rds_conn()
        # create cursor to traverse local database
        self.rds_cursor = self.rds_conn.cursor()

        # create a null variable to store the suppliers
        self.suppliers = None

        # creates arrays to store the filtered suppliers in a drop down-list as well as their respective ids
        self.filtered_suppliers = []
        self.filtered_supplier_ids = []

        # create text entry variable and make it empty.
        self.supplier = tk.StringVar()
        self.supplier.set("")

        # creates a label asking for the supplier name and places this label in the centre-left part of screen
        self.supplier_name = tk.Label(master=self)
        self.supplier_name.config(text="Who's the Supplier?")
        self.supplier_name.grid(row=1, column=0)

        # creates text entry bar for supplier, places text entry bar to the right of "supplier Name" label
        # sets the text in entry bar to be an entry variable, and filters the drop-down list everytime a key is pressed
        self.supplier_bar = tk.Entry(master=self)
        self.supplier_bar.grid(row=1, column=1)  #
        self.supplier_bar.config(textvariable=self.supplier)
        self.supplier_bar.bind('<KeyRelease>', self.check_key)

        # creates button to go to the next page (selected task), places forward button at the bottom right of screen
        # if a list item is highlighted, then the forward button is clicked, select it
        self.forward_button = tk.Button(master=self)
        self.forward_button.config(width=20, text="Forward")
        self.forward_button.grid(row=3, column=3, padx=10, pady=10, sticky="SE")
        self.forward_button.bind("<Button-1>", self.supplier_selection)

        # button to go to the previous page (task selection page), places back button at the bottom left of screen
        self.back_button = tk.Button(master=self)
        self.back_button.config(width=20, text="Back", command=lambda: self.controller.show_page(4))
        self.back_button.grid(row=3, column=0, padx=10, pady=10, sticky="SW")

        # creates scrollbar to manage there are many suppliers, puts scrollbar to the bottom-right of supplier text box
        self.supplier_scrollbar = tk.Scrollbar(master=self)
        self.supplier_scrollbar.grid(row=2, column=2, padx=10, pady=10, sticky="NS")

        # creates a box to show a filtered list of suppliers based on keyboard input, attaches list to scrollbar
        self.supplier_list = tk.Listbox(master=self)
        self.supplier_list.config(yscrollcommand=self.supplier_scrollbar.set)

        # attaches scrollbar to list
        self.supplier_scrollbar.config(command=self.supplier_list.yview)

        # if a list item is double tapped, select it, place listbox to the left of scrollbar.
        # start with empty list
        self.supplier_list.bind("<Double-1>", self.supplier_selection)
        self.supplier_list.grid(row=2, column=1, padx=10, pady=10)
        self.list_update(self.filtered_suppliers)

        # filters the list based on current characters in text entry box.
        # If box is empty, empty the list (to reduce potential queries from the web)

    def check_key(self, event):
        # gets the text currently in the entry box
        value = event.widget.get()

        # if text is empty, empty the list
        if value == '':
            # keep supplier list empty if no key has been entered to save query costs
            # keep supplier id list empty if no key has been entered
            self.filtered_suppliers = []
            self.filtered_supplier_ids = []
        # if not, start with an empty array.
        # Then, add suppliers to the array if their id contains the phrase in the entry box
        else:
            self.filtered_suppliers = []
            self.filtered_supplier_ids = []
            for item in self.suppliers:
                if value.lower() in item[1].lower():
                    self.filtered_suppliers.append(item[1])
                    self.filtered_supplier_ids.append(item[0])

        # update data in list with all the suppliers in the array
        self.list_update(self.filtered_suppliers)

    def list_update(self, data):
        # clear previous data
        self.supplier_list.delete(0, 'end')

        # put in new data, append each item in the list (insert each item at the end of the list)
        for item in data:
            self.supplier_list.insert('end', item)

    def supplier_selection(self, event):
        # returns the index of the item chosen as listed in the original list
        index = self.supplier_list.curselection()[0]

        # if a supplier in the list is selected, then update the text variable with the name selected
        for i in self.supplier_list.curselection():
            self.supplier.set(self.supplier_list.get(i))

        # Return the supplier of the given index (this accounts for duplicates)
        self.chosen_supplier = self.filtered_suppliers[index]
        self.controller.selected_supplier_id = self.filtered_supplier_ids[index]

        # show the page for the corresponding task selected on the previous page
        self.complete_task()

        # filters the list, so if supplier comes back from next page, they see only 1 item
        data = [self.chosen_supplier]
        self.list_update(data)

    # finds all suppliers in database and saves them as the original list of suppliers
    def load_supplier_list(self):
        # 1 is None, so don't include 1.
        self.rds_cursor.execute("SELECT * from suppliers WHERE supplier_id > ?", (1,))
        self.suppliers = self.rds_cursor.fetchall()

    # load the emotion page with all the listed emotion choices.
    def complete_task(self):
        self.controller.frames[-2][1].update_emotion_list()
        self.controller.show_page(-2)
