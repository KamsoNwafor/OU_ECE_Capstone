import tkinter as tk
from tkinter import ttk
from Database import DatabaseManager as dbm

class ItemSelectionFrame(tk.Frame):
    chosen_battery = None
    frame_index = 4

    def __init__(self, master, controller):
        # Initialize the frame with a light gray background
        tk.Frame.__init__(self, master, bg="#fafafa")
        self.controller = controller

        # Connect to RDS database
        self.rds_conn = dbm.get_rds_conn()
        # Create a cursor to execute queries on the RDS database
        self.rds_cursor = self.rds_conn.cursor()

        # Initialize variables for battery data
        self.batteries = None
        self.filtered_batteries = []
        self.filtered_battery_ids = []

        # Create header frame with a green background and title
        header = tk.Frame(self, bg="#4CAF50")
        header.pack(fill="x")
        tk.Label(header, text="Step 3: Battery Selection", font=("Roboto", 14, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(pady=15)

        # Create content frame with a subtle border and light gray background
        content = tk.Frame(self, bg="#f0f0f0", bd=1, relief="solid")
        content.pack(pady=10, padx=10, fill="both", expand=True)

        # Selected user label
        self.user_name = tk.Label(content, font=("Roboto", 11), bg="#f0f0f0", fg="#333333")
        self.user_name.grid(row=0, column=1, pady=(10, 5))

        # Battery label
        self.battery_name = tk.Label(content, text="Enter Battery Here, or Scan Barcode", font=("Roboto", 11), bg="#f0f0f0", fg="#333333")
        self.battery_name.grid(row=1, column=1, pady=(5, 5))

        # Battery entry
        self.battery = tk.StringVar()
        self.battery.set("")
        self.battery_bar = ttk.Entry(content, textvariable=self.battery)
        self.battery_bar.grid(row=2, column=1, pady=5)
        self.battery_bar.bind('<KeyRelease>', self.check_key)

        # Battery list with scrollbar
        self.battery_scrollbar = tk.Scrollbar(content, orient="vertical")
        self.battery_scrollbar.grid(row=3, column=2, padx=(0, 10), pady=10, sticky="NS")

        self.battery_list = tk.Listbox(content, yscrollcommand=self.battery_scrollbar.set, font=("Roboto", 11))
        self.battery_scrollbar.config(command=self.battery_list.yview)
        self.battery_list.grid(row=3, column=1, padx=10, pady=10)
        self.battery_list.bind("<Double-1>", self.battery_selection)
        self.list_update(self.filtered_batteries)

        # Navigation buttons frame
        nav_frame = tk.Frame(content, bg="#f0f0f0")
        nav_frame.grid(row=4, column=0, columnspan=3, pady=10)

        # Back button to return to the previous page
        self.back_button = ttk.Button(nav_frame, text="Back", style="Secondary.TButton", command=lambda: controller.back_button())
        self.back_button.pack(side="left", padx=5)

        # Forward button to proceed with battery selection
        self.forward_button = ttk.Button(nav_frame, text="Forward", style="Primary.TButton", command=lambda: self.battery_selection(None))
        self.forward_button.pack(side="left", padx=5)

    def check_key(self, event):
        # Get the current text in the entry box
        value = event.widget.get()
        # If the entry is empty, clear the filtered lists
        if value == '':
            self.filtered_batteries = []
            self.filtered_battery_ids = []
        else:
            # Filter batteries based on the entered text
            self.filtered_batteries = []
            self.filtered_battery_ids = []
            for item in self.batteries:
                if value.lower() in item[1].lower():
                    self.filtered_batteries.append(item[1])
                    self.filtered_battery_ids.append(item[0])
        # Update the listbox with filtered batteries
        self.list_update(self.filtered_batteries)

    def list_update(self, data):
        # Clear the listbox
        self.battery_list.delete(0, 'end')
        # Populate the listbox with new data
        for item in data:
            self.battery_list.insert('end', item)

    def update_user(self):
        # Query the database for the selected user's name
        self.rds_cursor.execute("select first_name, last_name from employees where user_id = ?", (self.controller.selected_user_id,))
        result = self.rds_cursor.fetchall()
        # Display the user's full name
        employee_name = f"{result[0][0]} {result[0][1]}"
        self.user_name.config(text=f"Selected User: {employee_name}")

    def battery_selection(self, event):
        # Handle battery selection for tasks other than new item intake (task ID 21)
        if self.controller.selected_task_id != "21":
            if self.filtered_batteries and self.battery_list.curselection():
                # Get the index of the selected battery
                index = self.battery_list.curselection()[0]
                # Update the entry field with the selected battery
                for i in self.battery_list.curselection():
                    self.battery.set(self.battery_list.get(i))
                # Store the selected battery and its serial number
                self.chosen_battery = self.filtered_batteries[index]
                self.controller.selected_battery_serial_number = self.filtered_battery_ids[index]
                # Navigate to the appropriate task page
                self.show_task_page()
                # Update the list to show only the selected battery
                data = [self.chosen_battery]
                self.list_update(data)
        else:
            # For new item intake, store the entered description and navigate to the new item page
            self.controller.input_battery_desc = self.battery.get()
            self.controller.frames[9][1].set_description()
            self.controller.show_page(9)

    def show_task_page(self):
        # Navigate to the appropriate page based on the selected task ID
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
        # Load all battery serial numbers and descriptions from the database
        self.rds_cursor.execute("select serial_number, part_description from batteries")
        self.batteries = self.rds_cursor.fetchall()

    def bind_double_click(self):
        # Bind double-click to battery selection for tasks other than new item intake
        if self.controller.selected_task_id != "21":
            self.battery_list.bind("<Double-1>", self.battery_selection)

    def previous_page(self):
        # Navigate back to the task selection page (index 3) and clear the selected task
        self.controller.show_page(3)
        self.controller.selected_task_id = None
