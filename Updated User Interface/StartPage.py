import tkinter as tk
from Database import DatabaseManager as dbm
from mariadb import Error

# TODO: Network Connection Option after else
# TODO: Handle Improper Network Connections

# import the tk.Frame class that creates frames
class StartFrame(tk.Frame):
    frame_index = 0

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master) # initialise the imported class

        self.controller = controller # store an instance of controller in frame, easier to manage controller data

        self.start_label = tk.Label(master = self)
        self.start_label.config(text="Spiers New Technologies")
        self.start_label.grid(row = 0, column = 1, padx = (300, 300), pady = 10) # leave a gap of 300 pixels to the left and 400 pixels to the right of start page label

        self.start_button = tk.Button(master = self)
        self.start_button.config(width=25, text="Start", command = self.manage_connection_status) # set Start button width to be 25% of screen width, then add a command to go to next page when clicked
        self.start_button.grid(row = 1, column = 1, padx = (300, 300), pady = 10) # leave a gap of 300 pixels to the left and 400 pixels to the right of start button

    def manage_connection_status(self):
        # local_conn = dbm.get_local_conn()
        rds_conn = dbm.get_rds_conn()

        # if local_conn.isconnected() or rds_conn.isconnected():

        connection_status = False

        # Check if the connection is alive
        try:
            # Try pinging the database to see if the connection is still open
            # local_conn.ping()  # This will attempt to reconnect if needed
            rds_conn.ping()  # This will attempt to reconnect if needed
            print("Connection is open!")
            connection_status = True  # Connection is good
            self.controller.frames[1][1].load_user_list()
        except Error as e:
            print("Connection lost or failed.")
            connection_status = False  # Connection failed

        finally:
            if connection_status:
                self.controller.forward_button()
            else:
                pass


