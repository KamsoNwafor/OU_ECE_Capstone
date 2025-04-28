import tkinter as tk
from tkinter import ttk
from Database import DatabaseManager as dbm
from mariadb import Error
from PIL import Image, ImageTk
import os

class StartFrame(tk.Frame):
    frame_index = 0

    def __init__(self, master, controller):
        # Initialize the StartFrame with a light background
        tk.Frame.__init__(self, master, bg="#fafafa")
        self.controller = controller
        self.bg_logo = None
        self.bg_label = None

        self.pack(fill="both", expand=True)

        # Create a green header bar with highlighted border
        header = tk.Frame(self, bg="#4CAF50", bd=0, relief="raised", highlightthickness=2, highlightbackground="#388E3C")
        header.pack(fill="x")

        # Add the "Spiers New Technologies" title inside the header
        title_frame = tk.Frame(header, bg="#4CAF50")
        title_frame.pack(pady=10)  # slightly reduced vertical space

        tk.Label(title_frame, text="Spiers", font=("Roboto", 16, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(side="left")
        tk.Label(title_frame, text="New", font=("Roboto", 16, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(side="left")
        tk.Label(title_frame, text="Technologies", font=("Roboto", 16, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(side="left")

        # Create a main content frame below the header
        content = tk.Frame(self, bg="#f0f0f0", bd=1, relief="solid")
        content.pack(pady=(5, 10), padx=10, fill="both", expand=True)

        # Load and set a faint background logo
        self.setup_background(content)

        # Add welcome message
        self.start_label = tk.Label(content, text="Welcome to the SPIERS Smart System",
                                    font=("Roboto", 12, "bold"), bg="#f0f0f0", fg="#212121")
        self.start_label.pack(pady=(5, 10))

        # Create a frame for navigation buttons
        nav_frame = tk.Frame(content, bg="#f0f0f0")
        nav_frame.pack(pady=5)

        # Start button to proceed
        self.start_button = ttk.Button(nav_frame, text="Start", style="Primary.TButton", command=self.manage_connection_status)
        self.start_button.pack(side="left", padx=5)

    def setup_background(self, parent):
        """Load and place a faded logo in the background."""
        try:
            logo_path = os.path.join(os.path.dirname(__file__), "logo.jpg")
            if os.path.exists(logo_path):
                original = Image.open(logo_path)
                faded = original.resize((500, 180))  # slightly reduced height for better balance
                faded = faded.convert("RGBA")

                alpha = faded.split()[3]
                alpha = alpha.point(lambda p: p * 0.2)  # Apply transparency
                self.bg_logo = ImageTk.PhotoImage(faded)

                # Center the faded logo slightly higher
                self.bg_label = tk.Label(parent, image=self.bg_logo, bg="#f0f0f0")
                self.bg_label.place(relx=0.5, rely=0.45, anchor='center')
        except Exception as e:
            print(f"Background logo setup failed: {e}")

    def manage_connection_status(self):
        """Check database connection and proceed if successful."""
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
