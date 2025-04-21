import tkinter as tk
from Database import DatabaseManager as dbm

# TODO: Handle Password Value Error in password_check()

# import the tk.Frame class that creates frames
class PasswordFrame(tk.Frame):

    is_correct_password = False

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master) # initialise the imported class

        self.controller = controller  # store an instance of controller in frame, easier to manage controller data

        # self.local_conn = dbm.get_local_conn()  # connect to local database
        # self.local_cursor = self.local_conn.cursor()  # create cursor to search through local database

        self.rds_conn = dbm.get_aws_conn()  # connect to local database
        self.rds_cursor = self.rds_conn.cursor()  # create cursor to search through local database

        self.password_tuple = None # all queries return tuples
        self.correct_password = None  # create a null variable to store the password string

        self.user_warehouse = tk.Label(master = self) # store selected warehouse
        self.user_warehouse.grid(row = 0, column = 0) # display selected warehouse on top left side of screen

        self.user_name = tk.Label(master=self) # store selected user from previous page
        self.user_name.grid(row=0, column=1) # display selected warehouse on top centre side of screen

        self.user_password = tk.Label(master = self) # label asking for password
        self.user_password.config(text="Password")
        self.user_password.grid(row=1, column = 0) # places this label in the centre-left part of screen

        self.password_text = tk.StringVar()  # create text input variable for password
        self.password_text.set("")  # set password text input variable to be entry

        self.password_bar = tk.Entry(master = self) # text entry bar for username
        self.password_bar.config(textvariable=self.password_text, show = "*")
        self.password_bar.grid(row=1, column=1) # places text entry bar to the right of "Name" label

        self.forward_button = tk.Button(master=self) # button to go to the next page (password page)
        self.forward_button.config(width=20, text="Forward", command=lambda: self.password_update()) # tries to update password, or tell user that password is wrong
        self.forward_button.grid(row=2, column=2, padx=10, pady=10, sticky="SE") # places forward button at the bottom right of screen

        self.back_button = tk.Button(master=self) # button to go to the next page (password page)
        self.back_button.config(width=20, text="Back", command=lambda: controller.back_button())
        self.back_button.grid(row=2, column=0, padx=10, pady=10, sticky="SW") # places back button at the bottom left of screen

    def password_update(self):
        self.password_check()

        if self.is_correct_password:
            self.controller.selected_password = self.password_text.get()
            self.controller.forward_button()
        else:
            pass

    def password_check (self):
        if self.password_text.get() == self.correct_password:
            self.is_correct_password = True
        else:
            self.is_correct_password = False

    def update_user(self):
        # self.local_cursor.execute("""select first_name, last_name, warehouse_id from employees where user_id = ?""", (self.controller.selected_user_id,))
        # result = self.local_cursor.fetchall()
        self.rds_cursor.execute("""select first_name, last_name, warehouse_id from employees where user_id = ?""", (self.controller.selected_user_id,))
        result = self.rds_cursor.fetchall()
        employee_name = f"{result[0][0]} {result[0][1]}"
        user_warehouse_id = result[0][2]
        self.user_name.config(text="Selected User Name: " + employee_name)

        # self.local_cursor.execute("""select warehouse_desc from warehouses where warehouse_id = ?""", (user_warehouse_id,))
        # result = self.local_cursor.fetchall()
        self.rds_cursor.execute("""select warehouse_desc from warehouses where warehouse_id = ?""", (user_warehouse_id,))
        result = self.rds_cursor.fetchall()
        user_warehouse = result[0][0]
        self.user_warehouse.config(text="Selected Warehouse: " + user_warehouse)
        # edits the user_warehouse variable so it displays what warehouse the user selected.

    def load_correct_password(self):
        # self.local_cursor.execute("select password from employees where user_id = ?", (self.controller.selected_user_id,))  # retrieves all data related to employee table in database
        # self.password_tuple = self.local_cursor.fetchall()  # retrieves users in database

        self.rds_cursor.execute("select password from employees where user_id = ?", (self.controller.selected_user_id,))  # retrieves all data related to employee table in database
        self.password_tuple = self.rds_cursor.fetchall()  # retrieves users in database

        self.correct_password = self.password_tuple[0][0]