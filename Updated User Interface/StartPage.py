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
        
        # Configure root window for a smaller size (600x360 pixels)
        self.title("SPIERS Smart System")
        self.geometry("600x360")
        self.configure(bg="#fafafa")
        self.minsize(400, 300)
        self.resizable(True, True)
        
        # Configure styles with smaller fonts and padding
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", font=("Roboto", 7), padding=4)
        self.style.configure("Primary.TButton", background="#4CAF50", foreground="#FFFFFF")
        self.style.configure("Secondary.TButton", background="#B0BEC5", foreground="#000000")
        self.style.configure("Exit.TButton", background="#F44336", foreground="#FFFFFF")
        self.style.map("Primary.TButton", background=[("active", "#388E3C")])
        self.style.map("Secondary.TButton", background=[("active", "#90A4AE")])
        self.style.map("Exit.TButton", background=[("active", "#D32F2F")])
        self.style.configure("TCombobox", font=("Roboto", 7), padding=2)
        self.style.configure("TEntry", font=("Roboto", 7))
        self.style.configure("TCheckbutton", font=("Roboto", 7))
        self.style.configure("TRadiobutton", font=("Roboto", 7))
        
        # Creating a container frame to store all the page frames
        container = tk.Frame(self, bg="#fafafa")
        container.pack(fill=tk.BOTH, expand=True)
        
        # Configure container to center its content
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
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
            
            # Ensure each frame centers its content
            frame.grid(row=0, column=0, sticky="nsew")
            
            index += 1
        
        self.show_page(0)
    
    def show_page(self, cont):
        frame = self.frames[cont]
        self.curr_frame = cont
        frame[1].tkraise()
    
    def forward_button(self):
        self.show_page(self.curr_frame + 1)  # Always move to the next frame
    
    def back_button(self):
        self.show_page(self.curr_frame - 1)

    def validate_and_proceed(self, current_index, next_index, validation_field, field_name):
        from tkinter import messagebox
        if isinstance(validation_field, bool):
            if not validation_field:
                messagebox.showerror("Missing Information", f"Please complete: {field_name}", parent=self)
                return
        elif not validation_field.strip():
            messagebox.showerror("Missing Information", f"Please complete: {field_name}", parent=self)
            return
        self.show_page(next_index)

if __name__ == "__main__":
    dbm.setup_rds_database()
    root = App()
    root.mainloop()
