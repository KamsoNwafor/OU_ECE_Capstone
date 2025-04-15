import tkinter as tk
from Database import DatabaseData

class PasswordFrame(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        user_data = DatabaseData()
        self.users = user_data.get_users()

        self.controller = controller

        self.user_warehouse = tk.Label(master = self)
        self.user_warehouse.config(text="Selected Warehouse: " + self.controller.selected_warehouse)
        self.user_warehouse.grid(row = 0, column = 0)

        self.user_name = tk.Label(master = self)
        self.user_name.config(text="First Name")
        self.user_name.grid(row=1, column = 1)

        self.name_bar = tk.Entry(master = self)
        self.name_bar.config()
        self.name_bar.grid(row=1, column=2)

        self.missing_name = tk.Label(master = self)
        self.missing_name.config (text = "If your name is not listed, please contact your supervisor")
        self.missing_name.grid(row = 2, column = 2)

        self.forward_button = tk.Button(master=self)
        self.forward_button.config(width=20, text="Forward", command=lambda: controller.forward_button())
        self.forward_button.grid(row=3, column=3, padx=10, pady=10, sticky="SE")

        self.back_button = tk.Button(master=self)
        self.back_button.config(width=20, text="Back", command=lambda: controller.back_button())
        self.back_button.grid(row=3, column=0, padx=10, pady=10, sticky="SW")

        self.forward_button = tk.Button

    def update_warehouse(self):
        self.user_warehouse.config(text="Selected Warehouse: " + self.controller.selected_warehouse)