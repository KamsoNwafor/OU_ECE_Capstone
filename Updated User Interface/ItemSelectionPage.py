import tkinter as tk
from tkinter import ttk
from Database import DatabaseManager as dbm

class ItemSelectionFrame(tk.Frame):
    frame_index = 4

    def __init__(self, master, controller):
        # Initialize the frame with a light gray background
        tk.Frame.__init__(self, master, bg="#fafafa")
        self.controller = controller

        # Connect to RDS database
        self.rds_conn = dbm.get_rds_conn()
        self.rds_cursor = self.rds_conn.cursor()

        # Initialize variables for battery data
        self.batteries = None
        self.filtered_battery_ids = []

        # Header frame with a green background and title
        header = tk.Frame(self, bg="#4CAF50")
        header.pack(fill="x")
        tk.Label(header, text="Battery Selection", font=("Roboto", 14, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(pady=10)

        # Content frame with a subtle border and light gray background
        content = tk.Frame(self, bg="#f0f0f0", bd=1, relief="solid")
        content.pack(pady=5, padx=5, fill="x", expand=False)
        content.grid_columnconfigure(1, weight=1)

        # Selected user label
        self.user_name = tk.Label(content, font=("Roboto", 11), bg="#f0f0f0", fg="#333333")
        self.user_name.grid(row=0, column=1, pady=(10, 5))

        # Battery label
        self.battery_name = tk.Label(content, text="Enter Battery Here, or Scan Barcode", font=("Roboto", 11), bg="#f0f0f0", fg="#333333")
        self.battery_name.grid(row=1, column=1, pady=(5, 5))

        # Battery entry box
        self.battery = tk.StringVar()
        self.battery.set("")
        self.battery_bar = ttk.Entry(content, textvariable=self.battery, font=("Roboto", 13))  # Bigger text
        self.battery_bar.grid(row=2, column=1, pady=4, ipady=4, sticky="ew")
        self.battery_bar.bind('<KeyRelease>', self.check_key)

        # Battery list with scrollbar (smaller height)
        self.battery_scrollbar = tk.Scrollbar(content, orient="vertical")
        self.battery_scrollbar.grid(row=3, column=2, padx=(0, 10), pady=(5, 5), sticky="NS")

        self.battery_list = tk.Listbox(content, yscrollcommand=self.battery_scrollbar.set, font=("Roboto", 11), height=6)
        self.battery_scrollbar.config(command=self.battery_list.yview)
        self.battery_list.grid(row=3, column=1, padx=10, pady=(5, 5), sticky="ew")

        # Load any available battery IDs initially
        self.list_update(self.filtered_battery_ids)

        # Navigation buttons frame
        nav_frame = tk.Frame(content, bg="#f0f0f0")
        nav_frame.grid(row=4, column=0, columnspan=3, pady=(8, 2))

        nav_frame.grid_columnconfigure(0, weight=1)
        nav_frame.grid_columnconfigure(1, weight=1)
        nav_frame.grid_columnconfigure(2, weight=1)

        # Back button
        self.back_button = ttk.Button(nav_frame, text="Back", style="Secondary.TButton", command=lambda: self.previous_page())
        self.back_button.grid(row=0, column=1, padx=5)

        # Forward button
        self.forward_button = ttk.Button(nav_frame, text="Forward", style="Primary.TButton", command=lambda: self.battery_selection(None))
        self.forward_button.grid(row=0, column=2, padx=5)

    def check_key(self, event):
        # Filter batteries based on the typed input
        value = event.widget.get()
        if value == '':
            self.filtered_battery_ids = []
        else:
            self.filtered_battery_ids = []
            for item in self.batteries:
                if value.lower() in item[0].lower():
                    self.filtered_battery_ids.append(item[0])
        self.list_update(self.filtered_battery_ids)

    def list_update(self, data):
        # Update the listbox with filtered batteries
        self.battery_list.delete(0, 'end')
        for item in data:
            self.battery_list.insert('end', item)

    def update_user(self):
        # Display the selected user's name
        self.rds_cursor.execute("SELECT first_name, last_name FROM employees WHERE user_id = ?", (self.controller.selected_user_id,))
        result = self.rds_cursor.fetchall()
        employee_name = f"{result[0][0]} {result[0][1]}"
        self.user_name.config(text=f"Selected User: {employee_name}")

    def battery_selection(self, event):
        # Handle battery selection
        if (self.battery.get() in self.filtered_battery_ids or self.battery_list.curselection()):
            if self.battery_list.curselection():
                index = self.battery_list.curselection()[0]
                for i in self.battery_list.curselection():
                    self.battery.set(self.battery_list.get(i))
                self.controller.selected_battery_serial_number = self.filtered_battery_ids[index]
            else:
                self.controller.selected_battery_serial_number = self.battery.get()
            self.show_task_page()
            data = [self.controller.selected_battery_serial_number]
            self.list_update(data)
        else:
            self.controller.selected_battery_serial_number = self.battery.get()
            self.controller.frames[9][1].set_serial_num()
            self.controller.show_page(9)

    def show_task_page(self):
        # Navigate to the correct task page based on task ID
        if self.controller.selected_task_id == "1":
            self.controller.frames[5][1].find_item()
            self.controller.show_page(5)
        elif self.controller.selected_task_id in ["2", "3"]:
            self.controller.frames[6][1].update_client_task_list()
            self.controller.show_page(6)
        elif self.controller.selected_task_id == "4":
            self.controller.frames[7][1].load_locations()
            self.controller.frames[7][1].load_current_location()
            self.controller.show_page(7)
        elif self.controller.selected_task_id == "20":
            self.controller.frames[8][1].image_preview()
            self.controller.show_page(8)

    def load_battery_list(self):
        # Load all batteries from the database
        self.rds_cursor.execute("SELECT serial_number, part_description FROM batteries")
        self.batteries = self.rds_cursor.fetchall()

    def bind_double_click(self):
        # Enable double-click for selection if not in new item intake
        if self.controller.selected_task_id != "21":
            self.battery_list.bind("<Double-1>", self.battery_selection)

    def previous_page(self):
        # Navigate back to the Task Selection page
        self.controller.show_page(3)
        self.controller.selected_task_id = None
