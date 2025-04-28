import tkinter as tk
from tkinter import ttk
from Database import DatabaseManager as dbm
from StartPage import StartFrame
from UserPage import UserFrame
from PasswordPage import PasswordFrame
from TaskSelectionPage import TaskSelectionFrame
from ItemSelectionPage import ItemSelectionFrame
from FindPage import FindFrame
from ClientPage import ClientFrame
from BatteryState import BatteryStateFrame
from BatteryStateActionPage import BatteryStateActionFrame
from MovePage import MoveFrame
from NewItemPage import NewItemFrame
from PicturePage import PictureFrame
from EmotionSelectionPage import EmotionSelectionFrame
from RequestPage import RequestFrame

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        # Configure root window
        self.title("Spiers New Technologies")
        self.geometry("800x480")
        self.configure(bg="#fafafa")
        self.minsize(400, 300)
        
        # Configure styles to match the original SPIERS project
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", font=("Roboto", 11), padding=10)
        self.style.configure("Primary.TButton", background="#4CAF50", foreground="#FFFFFF")
        self.style.configure("Secondary.TButton", background="#B0BEC5", foreground="#000000")  # Updated to gray
        self.style.configure("Exit.TButton", background="#F44336", foreground="#FFFFFF")  # Added exit button style
        self.style.map("Primary.TButton", background=[("active", "#388E3C")])
        self.style.map("Secondary.TButton", background=[("active", "#90A4AE")])  # Lighter gray for active state
        self.style.map("Exit.TButton", background=[("active", "#D32F2F")])  # Slightly darker red for active state
        self.style.configure("TCombobox", font=("Roboto", 11))
        self.style.configure("TEntry", font=("Roboto", 11))
        self.style.configure("TCheckbutton", font=("Roboto", 11))
        self.style.configure("TRadiobutton", font=("Roboto", 11))
        
        # Creating a container frame to store all the page frames
        container = tk.Frame(self, bg="#fafafa")
        container.pack(fill=tk.BOTH, expand=True)
        
        # Initializing page frames to an empty array
        self.frames = []
        self.curr_frame = 0
        
        # Controller variables
        self.selected_user_id = None
        self.selected_task_id = None
        self.selected_battery_serial_number = None
        self.selected_state_id = None
        self.selected_client_id = None
        self.selected_actions = None
        self.old_location_id = None
        self.selected_location_id = None
        self.selected_emotion = None
        self.selected_picture = None
        self.selected_part_number = None
        self.selected_item_type = None
        self.input_battery_desc = None
        
        # Iterating through page classes
        index = 0
        for F in (StartFrame, UserFrame, PasswordFrame, TaskSelectionFrame, ItemSelectionFrame,
                  FindFrame, ClientFrame, MoveFrame, PictureFrame, NewItemFrame,
                  BatteryStateFrame, BatteryStateActionFrame, EmotionSelectionFrame, RequestFrame):
            frame = F(container, self)
            frame_tuple = (index, frame)
            self.frames.append(frame_tuple)
            
            frame.grid_rowconfigure(0, weight=1)
            frame.grid_rowconfigure(1, weight=1)
            frame.grid_rowconfigure(2, weight=1)
            frame.grid_columnconfigure(0, weight=1)
            frame.grid_columnconfigure(1, weight=1)
            frame.grid_columnconfigure(2, weight=1)
            frame.grid(row=0, column=0, sticky="nsew")
            
            index += 1
        
        self.show_page(0)
    
    def show_page(self, cont):
        frame = self.frames[cont]
        self.curr_frame = cont
        frame[1].tkraise()
    
    def forward_button(self):
        self.show_page(self.curr_frame + 1)
    
    def back_button(self):
        self.show_page(self.curr_frame - 1)

if __name__ == "__main__":
    dbm.connect_rds()
    root = App()
    root.mainloop()