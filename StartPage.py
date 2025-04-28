


import tkinter as tk
from tkinter import ttk
from Database import DatabaseManager as dbm
from mariadb import Error
from PIL import Image, ImageTk
import os

class StartFrame(tk.Frame):
    frame_index = 0

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master, bg="#fafafa")  # Set soft background color
        self.controller = controller
        self.bg_logo = None
        self.bg_label = None

        # Create header with title
        header = tk.Frame(self, bg="#4CAF50")
        header.pack(fill="x")
        tk.Label(header, text="Spiers New Technologies", font=("Roboto", 16, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(pady=15)

        # Create content frame
        content = tk.Frame(self, bg="#f0f0f0", bd=1, relief="solid")
        content.pack(pady=10, padx=10, fill="both", expand=True)

        # Load and place the background logo if it exists
        self.setup_background(content)

        # Step indicator
        self.step_label = tk.Label(content, text="Step 1 of 6", font=("Roboto", 12), bg="#f0f0f0", fg="#212121")
        self.step_label.pack(pady=(10, 5))

        # Main title in content frame
        self.start_label = tk.Label(content, text="Welcome to the SPIERS Smart System", font=("Roboto", 12, "bold"), bg="#f0f0f0", fg="#212121")
        self.start_label.pack(pady=(5, 10))

        # Navigation buttons frame
        nav_frame = tk.Frame(content, bg="#f0f0f0")
        nav_frame.pack(pady=10)

        # Start Button
        self.start_button = ttk.Button(nav_frame, text="Start", style="Primary.TButton", command=self.manage_connection_status)
        self.start_button.pack(side="left", padx=5)

    def setup_background(self, parent):
        try:
            # Assuming logo image is in the same directory as the script
            logo_path = os.path.join(os.path.dirname(__file__), "spiers_logo.png")

            if os.path.exists(logo_path):
                original = Image.open(logo_path)
                faded = original.copy()
                faded = faded.resize((600, 300))
                faded = faded.convert("RGBA")
                alpha = faded.split()[3]
                alpha = alpha.point(lambda p: p * 0.2)  # Make it faint
                self.bg_logo = ImageTk.PhotoImage(faded)

                self.bg_label = tk.Label(parent, image=self.bg_logo, bg="#f0f0f0")
                self.bg_label.place(relx=0.5, rely=0.5, anchor='center')
        except Exception as e:
            print(f"Background logo setup failed: {e}")

    def manage_connection_status(self):
        rds_conn = dbm.get_rds_conn()
        connection_status = False

        try:
            rds_conn.ping()
            print("Connection is open!")
            connection_status = True
            self.controller.frames[1][1].load_user_list()
        except Error as e:
            print("Connection lost or failed.")
            connection_status = False

        finally:
            if connection_status:
                self.controller.forward_button()
            else:
                pass

