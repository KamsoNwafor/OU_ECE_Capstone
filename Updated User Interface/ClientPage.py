import tkinter as tk
from tkinter import ttk
from Database import DatabaseManager as dbm

# import the tk.Frame class that creates frames
class ClientFrame(tk.Frame):
    chosen_client = None
    frame_index = 6

    def __init__(self, master, controller):
        # initialise the imported class
        tk.Frame.__init__(self, master, bg="#fafafa")  # Set soft background color

        # store an instance of controller in frame, easier to manage controller data
        self.controller = controller

        # self.local_conn = dbm.get_local_conn()  # connect to database
        # self.local_cursor = self.local_conn.cursor()  # create cursor to traverse database

        # connect to local database
        self.rds_conn = dbm.get_rds_conn()
        # create cursor to traverse local database
        self.rds_cursor = self.rds_conn.cursor()

        self.status_buttons = None

        # create a null variable to store the clients
        self.clients = None

        # creates arrays to store the filtered clients in a drop down-list as well as their respective ids
        self.filtered_clients = []
        self.filtered_client_ids = []

        # Once again, I'm setting string variable to be None.
        # It's initalised in update_client_task_list.
        # I haven't touched anything else.

        # create text entry variable and make it empty.
        self.client = None

        # Create header with title
        header = tk.Frame(self, bg="#4CAF50")
        header.pack(fill="x")
        tk.Label(header, text="Step 5: Select Client", font=("Roboto", 14, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(pady=15)

        # Create content frame
        content = tk.Frame(self, bg="#f0f0f0", bd=1, relief="solid")
        content.pack(pady=10, padx=10, fill="both", expand=True)

        # creates a label asking for the client status and places this label in the top-left part of screen
        self.client_status = tk.Label(content, text="Customer or Supplier?", font=("Roboto", 12, "bold"), bg="#f0f0f0", fg="#212121")
        self.client_status.grid(row=0, column=0, pady=(10, 5), sticky="w")

        # a variable to track whether the client is a supplier or a customer
        self.status = None

        # variable to create buttons in list
        self.status_option = None

        # String Variable to store client options
        # Initial value must be different from options listed in order to avoid selection errors
        self.status_list = None

        # creates a label asking for the client name and places this label in the centre-left part of screen
        self.client_name = tk.Label(content, text="Who's the client?", font=("Roboto", 11), bg="#f0f0f0", fg="#333333")
        self.client_name.grid(row=2, column=0, pady=5, sticky="w")

        # creates text entry bar for client, places text entry bar to the right of "client Name" label
        # sets the text in entry bar to be an entry variable, and filters the drop-down list everytime a key is pressed
        self.client_bar = ttk.Entry(content)
        self.client_bar.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.client_bar.bind('<KeyRelease>', self.check_key)

        # creates scrollbar to manage there are many clients, puts scrollbar to the bottom-right of client text box
        self.client_scrollbar = ttk.Scrollbar(content, orient="vertical")
        self.client_scrollbar.grid(row=3, column=2, padx=(0, 10), pady=10, sticky="ns")

        # creates a box to show a filtered list of clients based on keyboard input, attaches list to scrollbar
        self.client_list = tk.Listbox(content, yscrollcommand=self.client_scrollbar.set, font=("Roboto", 11))
        self.client_list.grid(row=3, column=1, padx=(10, 0), pady=10, sticky="ew")

        # attaches scrollbar to list
        self.client_scrollbar.config(command=self.client_list.yview)

        # if a list item is double tapped, select it, place listbox to the left of scrollbar.
        # start with empty list
        self.client_list.bind("<Double-1>", self.client_selection)
        self.list_update(self.filtered_clients)

    # filters the list based on current characters in text entry box.
    # If box is empty, empty the list (to reduce potential queries from the web)
    def check_key(self, event):
        # gets the text currently in the entry box
        value = event.widget.get()

        # if text is empty, empty the list
        if value == '':
            # keep client list empty if no key has been entered to save query costs
            # keep client id list empty if no key has been entered
            self.filtered_clients = []
            self.filtered_client_ids = []
        # if not, start with an empty array.
        # Then, add clients to the array if their id contains the phrase in the entry box
        else:
            self.filtered_clients = []
            self.filtered_client_ids = []
            for item in self.clients:
                if value.lower() in item[1].lower():
                    self.filtered_clients.append(item[1])
                    self.filtered_client_ids.append(item[0])

        # update data in list with all the clients in the array
        self.list_update(self.filtered_clients)

    def list_update(self, data):
        # clear previous data
        self.client_list.delete(0, 'end')

        # put in new data, append each item in the list (insert each item at the end of the list)
        for item in data:
            self.client_list.insert('end', item)

    def client_selection(self, event=None):
        # makes sure a valid client was selected
        if self.filtered_clients and self.client_list.curselection():
            # returns the index of the item chosen as listed in the original list
            index = self.client_list.curselection()[0]

            # if a client in the list is selected, then update the text variable with the name selected
            for i in self.client_list.curselection():
                self.client.set(self.client_list.get(i))

            # Return the client of the given index (this accounts for duplicates)
            self.chosen_client = self.filtered_clients[index]
            self.controller.selected_client_id = self.filtered_client_ids[index]

            # show the page for the corresponding task selected on the previous page
            self.complete_task()

            # filters the list, so if client comes back from next page, they see only 1 item
            data = [self.chosen_client]
            self.list_update(data)

    # finds all clients in database and saves them as the original list of clients
    def load_client_list(self, value):
        # 1 is None, so don't include 1.
        self.rds_cursor.execute("SELECT * FROM clients WHERE client_id > %s AND client_status_id = %s ORDER BY client_id", (1, value))
        self.clients = self.rds_cursor.fetchall()

    # load the take picture page.
    def complete_task(self):
        if self.controller.selected_task_id == "2":
            self.controller.frames[10][1].update_state_list()
            self.controller.show_page(10)
        elif self.controller.selected_task_id == "3":
            self.controller.frames[8][1].image_preview()
            self.controller.show_page(8)

    def update_client_task_list(self):
        # searches for the client roles in the database
        self.rds_cursor.execute("SELECT * FROM client_status")

        # loads the main status into the status selection list
        self.status = self.rds_cursor.fetchall()

        self.client = tk.StringVar()
        self.client.set("")

        self.client_bar.config(textvariable=self.client)

        # String Variable to store client options
        # Initial value must be different from options listed in order to avoid selection errors
        self.status_list = tk.StringVar(self)
        self.status_list.set("0")

        # Add radiobuttons to the content frame
        content = self.client_status.master  # Get the content frame (parent of client_status)
        self.status_buttons = []
        index = 1
        for status in self.status:
            # creates a single-selection list for each status
            self.status_option = ttk.Radiobutton(content, text=status[1], variable=self.status_list, value=status[0], command=lambda value=status[0]: self.load_client_list(value))
            # place the choices in the centre, one after the other
            self.status_option.grid(row=index, column=0, padx=10, pady=5, sticky="w")
            self.status_buttons.append(self.status_option)
            index += 1

        # Navigation buttons
        nav_frame = tk.Frame(content, bg="#f0f0f0")
        nav_frame.grid(row=index, column=0, columnspan=3, pady=10)

        # button to go to the previous page (item selection page), places back button at the bottom left of screen
        self.back_button = ttk.Button(nav_frame, text="Back", style="Secondary.TButton", command=self.previous_page)
        self.back_button.pack(side="left", padx=5)

        # creates button to go to the next page (client selection page), places forward button at the bottom right of screen
        # if a list item is highlighted, then the forward button is clicked, select it
        self.forward_button = ttk.Button(nav_frame, text="Forward", style="Primary.TButton", command=self.client_selection)
        self.forward_button.pack(side="left", padx=5)

    def previous_page(self):
        # loads previous page (item selection)
        self.controller.show_page(4)

        # removes battery serial number that's stored
        self.controller.selected_battery_serial_number = None

        for option in self.status_buttons:
            option.destroy()

        self.status_list = None
        self.client = None
        self.filtered_clients = []
        self.filtered_client_ids = []
        self.list_update(self.filtered_clients)
