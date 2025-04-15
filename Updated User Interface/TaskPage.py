import tkinter as tk
from Database import DatabaseData

class TaskFrame(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        task_data = DatabaseData()
        self.tasks = task_data.get_tasks()