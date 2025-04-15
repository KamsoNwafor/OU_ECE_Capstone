import tkinter as tk

# import the tk.Frame class that creates frames
class StartFrame(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master) # initialise the imported class

        start_label = tk.Label(master = self)
        start_label.config(text="Spiers New Technologies")
        start_label.grid(row = 0, column = 1, padx = (300, 300), pady = 10) # leave a gap of 300 pixels to the left and 400 pixels to the right of start page label

        start_button = tk.Button(master = self)
        start_button.config(width=25, text="Start", command = controller.forward_button) # set Start button width to be 25% of screen width, then add a command to go to next page when clicked
        start_button.grid(row = 1, column = 1, padx = (300, 300), pady = 10) # leave a gap of 300 pixels to the left and 400 pixels to the right of start button