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
import os


class App(tk.Tk):
    DEBUG_MODE = False  # Turn OFF debug mode

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # Load your custom icon
        icon_path = os.path.join(os.path.dirname(__file__), "smalllogo.png")
        self.iconphoto(False, tk.PhotoImage(file=icon_path))

        
        # Configure root window
        self.title("Spiers New Technologies")
        self.geometry("770x480")
        self.configure(bg="#fafafa")
        self.minsize(770, 480)
        self.resizable(True, True)
        
        # Configure styles to match the original SPIERS project
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", font=("Roboto", 14), padding=8)
        self.style.configure("Primary.TButton", background="#4CAF50", foreground="#FFFFFF")
        self.style.configure("Secondary.TButton", background="#B0BEC5", foreground="#000000")
        self.style.configure("Exit.TButton", background="#F44336", foreground="#FFFFFF")
        self.style.map("Primary.TButton", background=[("active", "#388E3C")])
        self.style.map("Secondary.TButton", background=[("active", "#90A4AE")])
        self.style.map("Exit.TButton", background=[("active", "#D32F2F")])
        self.style.configure("TCombobox", font=("Roboto", 11))
        self.style.configure("TEntry", font=("Roboto", 11))
        self.style.configure("TCheckbutton", font=("Roboto", 11))
        self.style.configure("TRadiobutton", font=("Roboto", 11))
        
        # Create a main frame to hold the canvas and scrollbar
        main_frame = tk.Frame(self, bg="#fafafa")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create a canvas for scrolling
        self.canvas = tk.Canvas(main_frame, bg="#fafafa")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add a vertical scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure the canvas to use the scrollbar
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Create a frame inside the canvas to hold all page frames
        self.scrollable_frame = tk.Frame(self.canvas, bg="#fafafa")
        
        # Add the scrollable frame to a window in the canvas
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Bind the canvas to update the scroll region and frame size
        self.scrollable_frame.bind("<Configure>", self.update_scroll_region)
        self.canvas.bind("<Configure>", self.update_frame_size)  # ADDED: Bind canvas resize
        
        # Bind mouse wheel scrolling
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)  # Windows
        self.canvas.bind_all("<Button-4>", self.on_mousewheel)   # Linux
        self.canvas.bind_all("<Button-5>", self.on_mousewheel)   # Linux
        
        # Configure scrollable frame to center its content
        self.scrollable_frame.grid_rowconfigure(0, weight=1)
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        
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
            frame = F(self.scrollable_frame, self)
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
    
    def update_scroll_region(self, event):
        """Update the scroll region of the canvas when the frame size changes."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def update_frame_size(self, event):  # ADDED: Ensure scrollable_frame fills canvas viewport
        """Adjust the scrollable_frame size to match the canvas viewport."""
        canvas_width = event.width
        canvas_height = event.height
        # Set the scrollable_frame width to canvas width
        self.canvas.itemconfig(self.canvas_frame, width=canvas_width)
        # Set the scrollable_frame height to at least canvas height or content height
        content_height = self.scrollable_frame.winfo_reqheight()
        if content_height < canvas_height:
            self.canvas.itemconfig(self.canvas_frame, height=canvas_height)
        else:
            self.canvas.itemconfig(self.canvas_frame, height=content_height)
    
    def on_mousewheel(self, event):
        """Handle mouse wheel scrolling."""
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")
    
    def show_page(self, cont):
        frame = self.frames[cont]
        self.curr_frame = cont
        frame[1].tkraise()
        self.canvas.yview_moveto(0) 
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def forward_button(self):
        self.show_page(self.curr_frame + 1)
    
    def back_button(self):
        self.show_page(self.curr_frame - 1)

if __name__ == "__main__":
    dbm.connect_rds()
    root = App()
    root.mainloop()
