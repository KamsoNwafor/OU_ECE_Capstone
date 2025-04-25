import tkinter as tk
from Database import DatabaseManager as dbm
from StartPage import StartFrame
from UserPage import UserFrame
from PasswordPage import PasswordFrame
from TaskSelectionPage import TaskSelectionFrame
from ItemSelectionPage import ItemSelectionFrame
from FindPage import FindFrame
from ReceivePage import ReceiveFrame
from PicturePage import PictureFrame
from EmotionSelectionPage import EmotionSelectionFrame
from RequestPage import RequestFrame

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

        self.selected_user_id = None
        self.selected_task_id = None
        self.selected_battery_serial_number = None
        self.selected_state_id = None
        self.selected_supplier_id = None
        self.selected_emotion = None

        # iterating through a tuple consisting of the different page layouts
        index = 0
        for F in (StartFrame,  #0
                  UserFrame,  #1
                  PasswordFrame,  #2
                  TaskSelectionFrame,  #3
                  ItemSelectionFrame,  #4
                  FindFrame,  #5
                  ReceiveFrame, #6
                  PictureFrame, #7
                  EmotionSelectionFrame,  #8
                  RequestFrame): #9
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

#dbm.setup_local_database()
#dbm.close_connection(dbm.local_conn)
dbm.setup_rds_database()
#dbm.clear_everything()


root = App()
root.title("Spiers New Technologies")
root.geometry("800x480")

root.mainloop()
