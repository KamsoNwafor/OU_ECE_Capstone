import tkinter as tk
from tkinter import ttk
from Database import DatabaseManager as dbm

class ClientFrame(tk.Frame):
    chosen_client = None
    frame_index = 6

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master, bg="#fafafa")  # Set soft background color
        self.controller = controller

        # Database connection
        self.rds_conn = dbm.get_rds_conn()
        self.rds_cursor = self.rds_conn.cursor()

        # Variables
        self.clients = None
        self.filtered_clients = []
        self.filtered_client_ids = []
        self.client = tk.StringVar()
        self.client.set("")
        self.status = None
        self.status_option = None
        self.status_list = tk.StringVar(self)
        self.status_list.set("0")
        self.next_row = 2  # Start after client_status

        # UI Layout
        header = tk.Frame(self, bg="#4CAF50")
        header.pack(fill="x")
        tk.Label(header, text="Select Client", font=("Roboto", 14, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(pady=15)

        content = tk.Frame(self, bg="#f0f0f0", bd=1, relief="solid")
        content.pack(pady=10, padx=10, fill="both", expand=True)
        content.grid_columnconfigure(1, weight=1)
        content.grid_rowconfigure(2, weight=1)

        self.battery_serial = tk.Label(content, font=("Roboto", 11), bg="#f0f0f0", fg="#333333")
        self.battery_serial.grid(row=0, column=0, columnspan=3, pady=(10, 5))

        self.client_status = tk.Label(content, text="Customer or Supplier?", font=("Roboto", 12, "bold"), bg="#f0f0f0", fg="#212121")
        self.client_status.grid(row=1, column=0, columnspan=3, pady=(5, 5))

        self.client_name = tk.Label(content, text="What kind?", font=("Roboto", 11), bg="#f0f0f0", fg="#333333")
        self.client_name.grid(row=3, column=0, columnspan=3, pady=(10, 5))

        self.client_bar = ttk.Entry(content, textvariable=self.client)
        self.client_bar.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
        self.client_bar.bind('<KeyRelease>', self.check_key)

        self.client_scrollbar = ttk.Scrollbar(content, orient="vertical")
        self.client_scrollbar.grid(row=5, column=2, padx=(0, 10), pady=10, sticky="ns")

        # SHORTER Listbox: height = 3
        self.client_list = tk.Listbox(content, yscrollcommand=self.client_scrollbar.set, font=("Roboto", 11), height=3)
        self.client_list.grid(row=5, column=1, padx=(10, 0), pady=10, sticky="nsew")

        self.client_scrollbar.config(command=self.client_list.yview)
        self.client_list.bind("<Double-1>", self.client_selection)

        self.list_update(self.filtered_clients)

    def check_key(self, event):
        value = event.widget.get()
        if value == '':
            self.filtered_clients = []
            self.filtered_client_ids = []
        else:
            self.filtered_clients = []
            self.filtered_client_ids = []
            for item in self.clients:
                if value.lower() in item[1].lower():
                    self.filtered_clients.append(item[1])
                    self.filtered_client_ids.append(item[0])
        self.list_update(self.filtered_clients)

    def list_update(self, data):
        self.client_list.delete(0, 'end')
        for item in data:
            self.client_list.insert('end', item)

    def client_selection(self, event=None):
        if self.filtered_clients and self.client_list.curselection():
            index = self.client_list.curselection()[0]
            for i in self.client_list.curselection():
                self.client.set(self.client_list.get(i))
            self.chosen_client = self.filtered_clients[index]
            self.controller.selected_client_id = self.filtered_client_ids[index]
            self.complete_task()
            data = [self.chosen_client]
            self.list_update(data)

    def load_client_list(self, value):
        self.rds_cursor.execute("SELECT * FROM clients WHERE client_id > %s AND client_status_id = %s ORDER BY client_id", (1, value))
        self.clients = self.rds_cursor.fetchall()

    def complete_task(self):
        if self.controller.selected_task_id == "2":
            self.controller.frames[10][1].update_state_list()
            self.controller.show_page(10)
        elif self.controller.selected_task_id == "3":
            self.controller.frames[8][1].image_preview()
            self.controller.show_page(8)

    def update_client_task_list(self):
        self.rds_cursor.execute("SELECT * FROM client_status")
        self.status = self.rds_cursor.fetchall()

        content = self.client_status.master
        index = self.next_row
        for status in self.status:
            self.status_option = ttk.Radiobutton(content, text=status[1], variable=self.status_list, value=status[0], command=lambda value=status[0]: self.load_client_list(value))
            self.status_option.grid(row=index, column=0, columnspan=3, padx=10, pady=5, sticky="w")
            index += 1

        self.client_name.grid(row=index, column=0, columnspan=3, pady=(10, 5))
        self.client_bar.grid(row=index+1, column=1, padx=5, pady=5, sticky="ew")
        self.client_scrollbar.grid(row=index+2, column=2, padx=(0, 10), pady=10, sticky="ns")
        self.client_list.grid(row=index+2, column=1, padx=(10, 0), pady=10, sticky="nsew")

        # Navigation Buttons - moved slightly up
        nav_frame = tk.Frame(content, bg="#f0f0f0")
        nav_frame.grid(row=index+3, column=0, columnspan=3, pady=(0,5))

        self.back_button = ttk.Button(nav_frame, text="Back", style="Secondary.TButton", command=self.previous_page)
        self.back_button.pack(side="left", padx=5)

        self.forward_button = ttk.Button(nav_frame, text="Forward", style="Primary.TButton", command=self.client_selection)
        self.forward_button.pack(side="left", padx=5)

    def update_battery_info(self):
        self.rds_cursor.execute("SELECT serial_number, part_description FROM batteries WHERE serial_number = %s", (self.controller.selected_battery_serial_number,))
        result = self.rds_cursor.fetchall()
        if result:
            serial_num, part_desc = result[0]
            self.battery_serial.config(text=f"Selected Battery: {serial_num} ({part_desc})")
        else:
            self.battery_serial.config(text=f"Selected Battery: {self.controller.selected_battery_serial_number or 'None'} (Not Found)")

    def previous_page(self):
        self.controller.show_page(4)
        self.controller.selected_battery_serial_number = None
