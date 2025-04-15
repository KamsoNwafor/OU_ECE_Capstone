import tkinter as tk
from Database import DatabaseData

class UserFrame(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        user_data = DatabaseData()
        self.users = user_data.get_users()

        self.controller = controller

        self.user_warehouse = tk.Label(master = self)
        self.user_warehouse.grid(row = 0, column = 0)

        self.user_name = tk.Label(master = self)
        self.user_name.config(text="First Name")
        self.user_name.grid(row=1, column = 0)

        self.name_bar = tk.Entry(master = self)
        self.name_bar.config()
        self.name_bar.grid(row=1, column=1)

        self.missing_name = tk.Label(master = self)
        self.missing_name.config (text = "If your name is not listed, please contact your supervisor")
        self.missing_name.grid(row = 3, column = 2)

        self.forward_button = tk.Button(master=self)
        self.forward_button.config(width=20, text="Forward", command=lambda: controller.forward_button())
        self.forward_button.grid(row=4, column=3, padx=10, pady=10, sticky="SE")

        self.back_button = tk.Button(master=self)
        self.back_button.config(width=20, text="Back", command=lambda: controller.back_button())
        self.back_button.grid(row=4, column=0, padx=10, pady=10, sticky="SW")

        self.location = tk.StringVar()
        self.location.set("")

        self.user_scrollbar = tk.Scrollbar(master=self)
        self.user_scrollbar.grid(row=2, column=2, padx=10, pady=10, sticky="NEWS")

        self.name_bar.bind('<KeyRelease>', self.check_key)

        self.user_list = tk.Listbox(master=self)
        self.user_list.config(yscrollcommand=self.user_scrollbar.set)

        self.user_scrollbar.config(command=self.user_list.yview)

        self.user_list.bind("<Double-1>", self.user_selection)
        self.user_list.grid(row=2, column=1, padx=10, pady=10)
        self.list_update([])

    def check_key(self, event):

        value = event.widget.get()

        # get data from l
        if value == '':
            data = []
        else:
            data = []
            for item in self.users:
                if value.lower() in item.lower():
                    data.append(item)

        # update data in listbox
        self.list_update(data)

    def list_update(self, data):
        # clear previous data
        self.user_list.delete(0, 'end')

        # put new data
        for item in data:
            self.user_list.insert('end', item)

    def user_selection(self, event):
        for i in self.user_list.curselection():
            self.location.set(self.user_list.get(i))

        self.controller.selected_user = self.location.get()

        # Now update the PasswordFrame to reflect the selected User
        self.controller.frames[3][1].update_user()

        self.controller.forward_button()

    def update_warehouse(self):
        self.user_warehouse.config(text="Selected Warehouse: " + self.controller.selected_warehouse)