import tkinter as tk
import openpyxl as xl
from openpyxl import Workbook
from Database import DatabaseManager as dbm
from datetime import datetime

# Report Frame
class RequestFrame(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller

        # connect to local database and create cursor to traverse local database
        self.rds_conn = dbm.get_rds_conn()
        self.rds_cursor = self.rds_conn.cursor()

        # variables carried over from the controller, don't initialise any of them
        self.request_id = None
        self.curr_time = None
        self.request_timestamp = tk.StringVar()
        self.request_timestamp.set("")
        self.serial_num = None
        self.work_type_id = None
        self.user_id = None
        self.state_id = 1
        self.client_id = 1

        # variables to write a report
        self.emotion = None
        self.report = tk.StringVar()
        self.report.set("")
        
        # Variables to avoid gargbage collection
        self.result = None
        self.employee = None
        self.battery_state = None
        self.client = None
        self.battery_desc = None

        # set title of excel file to save reports in
        self.workbook_title = "Request Report.xlsx"

        # creates a workbook object, argument is the name of workbook
        try:
            self.wb = xl.load_workbook(self.workbook_title)
        ## if workbook doesn't exist, create new workbook, save with intended title, and load it again
        except FileNotFoundError:
            self.wb = Workbook()
            self.wb.save (self.workbook_title)
            self.wb = xl.load_workbook(self.workbook_title)

        # choose the sheet in excel file
        self.report_sheet = self.wb.active
        self.report_sheet.title = "Reports"

        self.request_title_cell = self.report_sheet["A1"]
        self.timestamp_title_cell = self.report_sheet["B1"]
        self.report_title_cell = self.report_sheet["C1"]

        if (self.request_title_cell.value != "Request ID" ## if title columns have wrong title, give them the right title
         or self.timestamp_title_cell.value != "Report Timestamp"
         or self.report_title_cell.value != "Report"):
            self.request_title_cell.value = "Request ID"
            self.timestamp_title_cell.value = "Report Timestamp"
            self.request_title_cell.value = "Request ID"
            self.report_title_cell.value = "Report"

        self.request_cell = None
        self.timestamp_cell = None
        self.report_cell = None

        self.report_label = tk.Label(master = self)
        self.report_label.config(text="Please Make Any Final Edits To The Report")
        self.report_label.grid(row = 0, column = 1, padx = 10, pady = 10)

        self.report_text = tk.Entry(master = self)
        self.report_text.config(textvariable=self.report)
        self.report_text.grid(row = 1, column = 1, padx = 10, pady = 10, sticky="we")

        self.submit_button = tk.Button(master = self)
        self.submit_button.config(width=20, text="Confirm", command=lambda: self.complete_report())
        self.submit_button.grid(row=2, column=2, padx=10, pady=10, sticky="SE")

        self.back_button = tk.Button(master=self)
        self.back_button.config(width=20, text="Back", command=lambda: self.controller.back_button())
        self.back_button.grid(row=2, column=0, padx=10, pady=10, sticky = "SW")

    def complete_report(self):
        self.submit_request()
        self.submit_report()
        self.close_app()

    def close_app(self):
        self.wb.save(self.workbook_title)
        self.controller.destroy()

    def load_report(self):
        self.rds_cursor.execute("""
                                SELECT request_id FROM requests
                                ORDER BY request_id DESC
                                LIMIT 1;
                                """)
        self.result = self.rds_cursor.fetchall()

        if not self.result:
            self.request_id = 1
        else:
            self.request_id = self.result[0][0] + 1

        self.curr_time = datetime.now()
        self.request_timestamp.set(self.curr_time.strftime("%Y-%m-%d %H:%M:%S"))

        self.serial_num = self.controller.selected_battery_serial_number
        self.work_type_id = self.controller.selected_task_id
        self.user_id = self.controller.selected_user_id
        self.emotion = self.controller.selected_emotion

        if self.controller.selected_state_id:
            self.state_id = self.controller.selected_state_id

        if self.controller.selected_client_id:
            self.client_id = self.controller.selected_client_id

        self.rds_cursor.execute("""SELECT part_description FROM batteries where serial_number = ?""",
                                (self.serial_num,))
        self.result = self.rds_cursor.fetchall()
        self.battery_desc = self.result[0][0]

        self.rds_cursor.execute("""SELECT first_name, last_name FROM employees where user_id = ?""", (self.user_id,))
        self.result = self.rds_cursor.fetchall()
        self.employee = f"{self.result[0][0]} {self.result[0][1]}"

        self.rds_cursor.execute("""SELECT client_desc FROM clients where client_id = ?""",
                                (self.client_id,))
        self.result = self.rds_cursor.fetchall()
        self.client = self.result[0][0]

        # if find is selected
        if self.work_type_id == "1":
            self.report.set(f"{self.employee} found {self.battery_desc}. Now {self.employee} is {self.emotion}")
        # if receive is selected
        elif self.work_type_id == "2":
            self.report.set(f"{self.employee} received {self.battery_desc} from {self.client}. Now {self.employee} is {self.emotion}")
        # if ship is selected
        elif self.work_type_id == "3":
            pass
        # if move is selected
        elif self.work_type_id == "4":
            pass
        # if update battery status is selected
        elif self.work_type_id == "5":
            pass
        # if take picture is selected
        elif self.work_type_id == "21":
            pass

    def submit_request(self):
        self.rds_cursor.execute(""" INSERT INTO requests VALUES(?, ?, ?, ?, ?, ?, ?); """,
                                (self.request_id,
                                 self.curr_time,
                                 self.serial_num,
                                 self.work_type_id,
                                 self.user_id,
                                 self.state_id,
                                 self.client_id))
        
        self.rds_cursor.execute(""" INSERT INTO reports VALUES(?, ?, ?); """,
                                (self.request_id,
                                 self.curr_time,
                                 self.report.get()))

        dbm.save_changes(self.rds_conn)

        self.rds_cursor.execute("""SELECT * FROM requests;""")
        self.result = self.rds_cursor.fetchall()
        print(self.result)

        self.rds_cursor.execute("""SELECT * FROM reports;""")
        self.result = self.rds_cursor.fetchall()
        print(self.result)

    def submit_report(self):
        self.request_cell = self.report_sheet[f"A{self.request_id + 1}"]
        self.timestamp_cell = self.report_sheet[f"B{self.request_id + 1}"]  # increment so cell titles are not over-written
        self.report_cell = self.report_sheet[f"C{self.request_id + 1}"]

        self.request_cell.value = self.request_id
        self.timestamp_cell.value = self.request_timestamp.get()  ## Assign values to cells
        self.report_cell.value = self.report.get()

        self.adjust_cell_width()

    def adjust_cell_width(self):
        for col in self.report_sheet.columns:  # Automatically Adjust Cell Width
            max_length = 0
            column = col[0].column_letter  # Get the column name
            for row in range(1, self.report_sheet.max_row + 1):
                cell = self.report_sheet[f"{column}{row}"]

                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))

            adjusted_width = (max_length + 2) * 1.2
            self.report_sheet.column_dimensions[column].width = adjusted_width
