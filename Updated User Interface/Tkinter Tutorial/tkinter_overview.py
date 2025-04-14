import tkinter as tk
from tkinter import *
from tkinter import ttk

"""
Cannot use both pack() and grid(). For customization, use grid
"""

start = tk.Tk()


def start_screen():
    # Initialize main window
    start.title("EV Battery Solutions")
    start.geometry("800x480")  ## resolution changed
    start.configure(bg="white")

    """
    login()
    mark_multiple_tasks()

    """
    w = Label(start, text="Spiers New Technologies")
    w.pack()

    button = tk.Button(start, text='Start', width=25, command=start.destroy)
    button.pack()

    list_creator()

    toolbar_menu()

    select_one_option()

    # Create Tkinter variables
    user_var = tk.StringVar()
    location_var = tk.StringVar()
    item_var = tk.StringVar()
    action_var = tk.StringVar()
    vibe_var = tk.StringVar()

    start.mainloop()


## Creates a bar for text entry. Use for entering names
def login():
    Label(start, text='First Name').grid(row=2)
    Label(start, text='Last Name').grid(row=3)
    e1 = Entry(start)
    e2 = Entry(start)
    e1.grid(row=2, column=1)
    e2.grid(row=3, column=1)


## Creates a list which can have multiple options marked. Use for old battery work
def mark_multiple_tasks():
    var1 = IntVar()
    Checkbutton(start, text='male', variable=var1).grid(row=4, sticky=W)
    var2 = IntVar()
    Checkbutton(start, text='female', variable=var2).grid(row=5, sticky=W)


## Creates a list which can have only one option marked. Use for initial option
## Fix glitch where hovering over option selects it.
def select_one_option():
    v = IntVar()
    Radiobutton(start, text='GfG', variable=v, value=1).pack(anchor=W)
    Radiobutton(start, text='MIT', variable=v, value=2).pack(anchor=W)


## Create lists where user can create one or more. Use for names in login option.
def list_creator():
    Lb = Listbox(start)
    Lb.insert(1, 'Python')
    Lb.insert(2, 'Java')
    Lb.insert(3, 'C++')
    Lb.insert(4, 'Any other')
    Lb.pack()


## Don't really know if it's necessary, but good feature to have
def toolbar_menu():
    menu = Menu(start)
    start.config(menu=menu)
    filemenu = Menu(menu)
    menu.add_cascade(label='File', menu=filemenu)
    filemenu.add_command(label='New')
    filemenu.add_command(label='Open...')
    filemenu.add_separator()
    filemenu.add_command(label='Exit', command=start.quit)
    helpmenu = Menu(menu)
    menu.add_cascade(label='Help', menu=helpmenu)
    helpmenu.add_command(label='About')

# Useful for entries
def combobox():
    selected_item = combo_box.get()
    label.config(text="Selected Item: " + selected_item)

def combo():
    start.title("Combobox Example")

    # Create a label
    label = tk.Label(start, text="Selected Item: ")
    label.pack(pady=10)

    # Create a Combobox widget
    combo_box = ttk.Combobox(start, values=["Option 1", "Option 2", "Option 3"])
    combo_box.pack(pady=5)

    # Set default value
    combo_box.set("Option 1")

    # Bind event to selection
    combo_box.bind("<<ComboboxSelected>>", combobox())