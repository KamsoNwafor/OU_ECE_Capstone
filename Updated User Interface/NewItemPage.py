import tkinter as tk
from Database import DatabaseManager as dbm

# import the tk.Frame class that creates frames
class NewItemFrame (tk.Frame):
    chosen_client = None
    frame_index = 6

    def __init__(self, master, controller):
        tk.Frame.__init__(self,master)

        self.controller = controller