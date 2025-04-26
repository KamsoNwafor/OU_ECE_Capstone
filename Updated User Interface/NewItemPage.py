import tkinter as tk
from Database import DatabaseManager as dbm

# import the tk.Frame class that creates frames
class NewItemFrame (tk.Frame):
    chosen_client = None
    frame_index = 9

    def __init__(self, master, controller):
        tk.Frame.__init__(self,master)

        self.controller = controller

        # connect to local database
        self.rds_conn = dbm.get_rds_conn()
        # create cursor to traverse local database
        self.rds_cursor = self.rds_conn.cursor()
        
        self.serial = tk.StringVar()
        self.serial.set("")

        self.part = tk.StringVar()
        self.part.set("")

        self.item_type = tk.StringVar()
        self.item_type.set("")

        self.desc = tk.StringVar()
        self.desc.set("")
        
        self.serial_label = tk.Label(master = self)
        self.serial_label.config (text = "Battery serial number")
        self.serial_label.grid (row=0, column=0)

        self.serial_entry = tk.Entry(master=self)
        self.serial_entry.config(textvariable=self.serial)
        self.serial_entry.grid(row=0, column=1, sticky = "w")

        self.part_label = tk.Label(master=self)
        self.part_label.config(text="Battery part number")
        self.part_label.grid(row=1, column=0)

        self.part_entry = tk.Entry(master=self)
        self.part_entry.config(textvariable=self.part)
        self.part_entry.grid(row=1, column=1, sticky = "w")

        self.item_type_label = tk.Label(master=self)
        self.item_type_label.config(text="Battery item type")
        self.item_type_label.grid(row=2, column=0)

        self.item_type_entry = tk.Entry(master=self)
        self.item_type_entry.config(textvariable=self.item_type)
        self.item_type_entry.grid(row=2, column=1, sticky = "w")

        self.desc_label = tk.Label(master=self)
        self.desc_label.config(text="Battery description")
        self.desc_label.grid(row=0, column=2)

        self.desc_entry = tk.Entry(master=self)
        self.desc_entry.config(textvariable=self.desc)
        self.desc_entry.grid(row=1, column=2, sticky ="ew")

        self.forward_button = tk.Button(master=self)  # button to go to the next page (task selection page)
        self.forward_button.config(width=20, text="Forward", command=lambda: self.manage_details())  # tries to update password, or tell user that password is wrong
        self.forward_button.grid(row=3, column=2, padx=10, pady=10, sticky="SE")  # places forward button at the bottom right of screen

        self.back_button = tk.Button(master=self)  # button to go to the previous page (username page)
        self.back_button.config(width=20, text="Back", command=lambda: self.previous_page())
        self.back_button.grid(row=3, column=0, padx=10, pady=10, sticky="SW")  # places back button at the bottom left of screen

    def previous_page(self):
        self.controller.show_page(4)
        self.controller.input_battery_desc = None
        self.desc.set("")

    def manage_details(self):
        self.controller.selected_battery_serial_number = self.serial.get()
        self.controller.selected_part_number = self.part.get()
        self.controller.selected_item_type = self.item_type.get()
        self.controller.input_battery_desc = self.desc.get()

        self.controller.frames[8][1].image_preview()
        self.controller.show_page(8)

    def set_description(self):
        self.desc.set(self.controller.input_battery_desc)