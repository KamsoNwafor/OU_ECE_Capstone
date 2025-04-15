import tkinter as tk

from StartPage import StartFrame
from WarehousePage import WarehouseFrame
from ReportPage import ReportFrame
from UserPage import UserFrame
from PasswordPage import PasswordFrame

# import the tk.Tk class that creates windows
class App (tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs) # initialise the imported class

        # creating a container frame to store all the page frames
        container = tk.Frame(self)
        container.pack(fill = tk.BOTH, expand = True) # fill window with container frame

        # initializing page frames to an empty array
        self.frames = []
        self.curr_frame = 0

        self.selected_warehouse = ""
        self.user_name = ""
        self.password = ""

        # iterating through a tuple consisting of the different page layouts
        index = 0
        for F in (StartFrame, WarehouseFrame, UserFrame, PasswordFrame, ReportFrame):
            # initializing frame of that object from relevant page with for loop
            frame = F(container, self)
            frame_tuple = (index, frame)

            self.frames.append(frame_tuple)

            frame.grid_rowconfigure(0, weight=1)  # Center row 0
            frame.grid_rowconfigure(1, weight=1)  # Center row 1
            frame.grid_rowconfigure(2, weight=1)  # Center row 2
            frame.grid_columnconfigure(0, weight=1)  # Center column 0
            frame.grid_columnconfigure(1, weight=1)  # Center column 1
            frame.grid_columnconfigure(2, weight=1)  # Center column 2
            frame.grid(row=0, column=0, sticky="nsew")

            index += 1

        self.show_page(0) # load Start Page

    # to display the current frame passed as a parameter
    def show_page(self, cont):
        frame = self.frames[cont] # choose page frame from frame array
        self.curr_frame = cont
        frame[1].tkraise() # load frame

        # common actions
    def forward_button(self):
        self.show_page(self.curr_frame + 1)

    def back_button(self):
        self.show_page(self.curr_frame - 1)

        # warehouse actions


root = App()
root.title("Spiers New Technologies")
root.geometry("800x480")

root.mainloop()