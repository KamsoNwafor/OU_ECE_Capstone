import tkinter as tk
from Database import DatabaseManager

# import the tk.Frame class that creates frames
class ItemFrame(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master) # initialise the imported class

        self.controller = controller

        self.serial_num = DatabaseManager.get_serial_num() # retrieves battery serial number in database

        self.serial_num_part_num = tk.Label(master=self)  # label displaying serial number and part number together
        self.serial_num_part_num.config(text= f"Serial Number: \n Part Number: ")
        self.serial_num_part_num.grid(row=0, column=0)  # places this label on the top-left part of screen

        self.item_type_num_total = tk.Label(master=self)  # label displaying item type and total quantity together
        self.item_type_num_total.config(text=f"Item Type \n Total Quantity: ")
        self.item_type_num_total.grid(row=0, column=1)  # places this label on the top-centre part of screen

        self.num_old_num_death_row = tk.Label(master=self)  # label displaying old and death row quantities together
        self.num_old_num_death_row.config(text=f"Old Quantity: \n Death Row Quantity:")
        self.num_old_num_death_row.grid(row=1, column=0)  # places this label on the centre-left part of screen

        self.location_old_location_death_row = tk.Label(master=self)  # label old and death row locations together
        self.location_old_location_death_row.config(text=f"Old Location: \n Death Row Location: ")
        self.location_old_location_death_row.grid(row=1, column=1)  # places this label on the centre part of screen

        self.part_desc_num_new_location_new = tk.Label(master=self)  # label displaying part description, new quantity, and new location
        self.part_desc_num_new_location_new.config(text=f"Old Location: \n Death Row Location: ")
        self.part_desc_num_new_location_new.grid(row=2, column=0)  # places this label on the bottom-left part of screen

        self.image = None


