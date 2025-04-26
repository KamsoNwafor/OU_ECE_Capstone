import tkinter as tk
from Database import DatabaseManager as dbm

# TODO: Prevent from going forward if not in list

# import the tk.Frame class that creates frames
class UserFrame(tk.Frame):
    chosen_user = None
    frame_index = 1

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master) # initialise the imported class

        self.controller = controller  # store an instance of controller in frame, easier to manage controller data

       # self.local_conn = dbm.get_local_conn()  # connect to local database
       # self.local_cursor = self.local_conn.cursor()  # create cursor to search through local database

        self.rds_conn = dbm.get_rds_conn()  # connect to local database
        self.rds_cursor = self.rds_conn.cursor()  # create cursor to search through local database

        self.users = None # create a null variable to store the users

        self.filtered_users = []  # creates array to store filtered warehouse in drop-down list
        self.filtered_user_ids = []  # creates array to store filtered warehouse IDs

        self.user_name = tk.Label(master = self) # label asking for username
        self.user_name.config(text="Username")
        self.user_name.grid(row=0, column = 1) # places this label in the centre-left part of screen

        self.employee = tk.StringVar()  # create text entry variable
        self.employee.set("")  # set text entry variable as entry

        self.name_bar = tk.Entry(master = self) # text entry bar for username
        self.name_bar.grid(row=1, column=1) # places text entry bar to the right of "Name" label
        self.name_bar.config(textvariable=self.employee)
        self.name_bar.bind('<KeyRelease>', self.check_key)  # filters the list everytime a key is pressed

        self.missing_name = tk.Label(master = self)
        self.missing_name.config (text = "If your name is not listed, please contact your supervisor") # informs the user to contact the supervisor if their name is not in the drop down
        self.missing_name.grid(row = 3, column = 1) # places at the bottom of screen

        self.forward_button = tk.Button(master=self) # button to go to the next page (password page)
        self.forward_button.config(width=20, text="Forward")
        self.forward_button.grid(row=4, column=2, padx=10, pady=10, sticky="SE") # places forward button at the bottom right of screen

        self.forward_button.bind("<Button-1>", self.user_selection)  # if a list item is highlighted, and the forward button is clicked, select it

        self.back_button = tk.Button(master=self)
        self.back_button.config(width=20, text="Back", command=lambda: self.previous_page()) # button to go to the previous page (warehouse page)
        self.back_button.grid(row=4, column=0, padx=10, pady=10, sticky="SW") # places back button at the bottom left of screen

        self.user_scrollbar = tk.Scrollbar(master=self) # creates scrollbar just in case there are a bunch of users shown
        self.user_scrollbar.grid(row=2, column=2, padx=10, pady=10, sticky="NS") # puts scrollbar to the bottom right of user text box

        self.user_list = tk.Listbox(master=self) # creates a box to show a filtered list of users based on keyboard input
        self.user_list.config(yscrollcommand=self.user_scrollbar.set) # attaches list to scrollbar

        self.user_scrollbar.config(command=self.user_list.yview) # attaches scrollbar to list

        self.user_list.bind("<Double-1>", self.user_selection) # if a list item is double tapped, select it
        self.user_list.grid(row=2, column=1, padx=10, pady=10) # place listbox to the left of scrollbar
        self.list_update(self.filtered_users) # start with empty list

    # filters the list based on current characters in text entry box. If box is empty, empty the list (to reduce potential queries from the web)
    def check_key(self, event):

        value = event.widget.get() # gets the text currently in the entry box

        # if text is empty, empty the list
        if value == '':
            self.filtered_users = [] # keep user list empty if no key has been entered to save query costs
            self.filtered_user_ids = [] # keep user id list empty if no key has been entered
        else: # if text is not empty
            self.filtered_users = []
            self.filtered_user_ids = []
            for item in self.users: # start with an empty array, then add users to the array if they contain the phrase in the entry box
                if value.lower() in f"{item[1]} {item[2]}".lower():
                    self.filtered_users.append(f"{item[1]} {item[2]}") # combine first and last names
                    self.filtered_user_ids.append(item[0]) # add user_ids of employees

        # update data in list with all the warehouses in the array
        self.list_update(self.filtered_users)

    def list_update(self, data):
        # clear previous data
        self.user_list.delete(0, 'end')

        # put in new data, append each item in the list (insert each item at the end of the list)
        for item in data:
            self.user_list.insert('end', item)

    def user_selection(self, event):
        # make sure that a valid user was clicked
        if self.filtered_users and self.user_list.curselection():
            index = self.user_list.curselection()[0]  # returns the index of the item chosen

            for i in self.user_list.curselection(): # curselection is "cursor selection"
                self.employee.set(self.user_list.get(i)) # if a user in the list is selected, then update the text variable with the name selected

            self.chosen_user = self.filtered_users[index]
            self.controller.selected_user_id = self.filtered_user_ids[index]  # Return the nth occurring user selection (this accounts for duplicates)

            # Now update the PasswordFrame to reflect the selected User
            self.controller.frames[2][1].update_user() # updated the password page to see what user they selected

            self.controller.frames[2][1].load_correct_password()  # load the relevant user's password to be compared with password entry

            self.controller.forward_button() # go to the next page (password page)

            data = [self.chosen_user]
            self.list_update(data)  # filters the list, so if user comes back from next page, they see only 1 item

    def load_user_list(self):
        # self.local_cursor.execute("select user_id, first_name, last_name from employees where warehouse_id = ?", (self.controller.selected_warehouse_id,))  # retrieves all data related to employee table in database
        # self.users = self.local_cursor.fetchall()  # retrieves users in database
        self.rds_cursor.execute("""select user_id, first_name, last_name from employees""")  # retrieves all data related to employee table in database
        self.users = self.rds_cursor.fetchall()  # retrieves users in database

    def previous_page(self):
        self.controller.show_page(0)