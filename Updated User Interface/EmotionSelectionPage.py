import tkinter as tk
from tkinter import ttk
from Database import DatabaseManager as dbm

class EmotionSelectionFrame(tk.Frame):
    frame_index = 12

    def __init__(self, master, controller):
        # Initialize the frame
        tk.Frame.__init__(self, master, bg="#fafafa")
        self.controller = controller

        # Connect to database
        self.rds_conn = dbm.get_rds_conn()
        self.rds_cursor = self.rds_conn.cursor()

        # Lists of emotions and adjectives
        self.emotions = ["Excited", "Tired", "Confident", "Frustrated", "Happy", "Bored"]
        self.adjectives = ["Challenging", "Rewarding", "Tiring", "Fun", "Stressful", "Interesting"]

        # Create header
        header = tk.Frame(self, bg="#4CAF50")
        header.pack(fill="x")
        tk.Label(header, text="Emotion Selection", font=("Roboto", 14, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(pady=10)

        # Create content area
        content = tk.Frame(self, bg="#f0f0f0", bd=1, relief="solid")
        content.pack(pady=5, padx=5, fill="x", expand=False)
        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=1)

        # Mad Libs preview sentence
        self.mad_libs_label = tk.Label(content, text="After working on this task, I feel [emotion] because it was a [adjective] experience!", 
                                       font=("Roboto", 12, "italic"), bg="#f0f0f0", fg="#333333", wraplength=400)
        self.mad_libs_label.grid(row=0, column=0, columnspan=2, pady=(10, 15))

        # Variables for selections
        self.emotion_list = tk.StringVar(self)
        self.emotion_list.set("0")
        self.emotion_list.trace_add("write", self.update_mad_libs)

        self.adjective_list = tk.StringVar(self)
        self.adjective_list.set("0")
        self.adjective_list.trace_add("write", self.update_mad_libs)

        self.forward_button = None
        self.back_button = None

        # Load radiobuttons
        self.update_emotion_list()

    def update_mad_libs(self, *args):
        # Update the Mad Libs sentence based on selections
        emotion = self.emotion_list.get() if self.emotion_list.get() != "0" else "[emotion]"
        adjective = self.adjective_list.get() if self.adjective_list.get() != "0" else "[adjective]"
        self.mad_libs_label.config(text=f"After working on this task, I feel {emotion} because it was a {adjective} experience!")

    def manage_option(self):
        # Proceed only if both selections are made
        if self.emotion_list.get() != "0" and self.adjective_list.get() != "0":
            self.controller.selected_emotion = self.emotion_list.get()
            self.controller.selected_adjective = self.adjective_list.get()
            self.controller.frames[-1][1].load_report()
            self.controller.show_page(-1)

    def previous_page(self):
        # Navigate logically to previous frame depending on the situation
        self.rds_cursor.execute("SELECT * FROM batteries WHERE serial_number = %s", (self.controller.selected_battery_serial_number,))
        result = self.rds_cursor.fetchall()
        if not result:
            self.controller.show_page(8)
        else:
            if self.controller.selected_task_id == "1":
                self.controller.show_page(5)
            else:
                self.controller.show_page(8)

    def update_emotion_list(self):
        content = self.mad_libs_label.master

        # Emotion label
        emotion_label = tk.Label(content, text="Choose your emotion:", font=("Roboto", 12, "bold"), bg="#f0f0f0", fg="#212121")
        emotion_label.grid(row=1, column=0, columnspan=2, pady=(5, 5))

        # Emotions in two columns
        split_point = (len(self.emotions) + 1) // 2
        for idx, emotion in enumerate(self.emotions):
            row = idx % split_point + 2
            column = idx // split_point
            emotion_option = ttk.Radiobutton(content, text=emotion, variable=self.emotion_list, value=emotion)
            emotion_option.grid(row=row, column=column, padx=10, pady=2, sticky="w")

        # Calculate next row start for adjectives
        max_row = (split_point if len(self.emotions) % 2 == 0 else split_point) + 2

        # Adjective label
        adjective_label = tk.Label(content, text="Choose an adjective:", font=("Roboto", 12, "bold"), bg="#f0f0f0", fg="#212121")
        adjective_label.grid(row=max_row, column=0, columnspan=2, pady=(10, 5))

        # Adjectives in two columns
        split_point_adj = (len(self.adjectives) + 1) // 2
        for idx, adjective in enumerate(self.adjectives):
            row = max_row + 1 + (idx % split_point_adj)
            column = idx // split_point_adj
            adjective_option = ttk.Radiobutton(content, text=adjective, variable=self.adjective_list, value=adjective)
            adjective_option.grid(row=row, column=column, padx=10, pady=2, sticky="w")

        # Navigation Buttons
        nav_frame = tk.Frame(content, bg="#f0f0f0")
        nav_frame.grid(row=max(max_row + split_point_adj, row) + 1, column=0, columnspan=2, pady=(10, 2))

        nav_frame.grid_columnconfigure(0, weight=1)
        nav_frame.grid_columnconfigure(1, weight=1)

        self.back_button = ttk.Button(nav_frame, text="Back", style="Secondary.TButton", command=self.previous_page)
        self.back_button.grid(row=0, column=0, padx=5)

        self.forward_button = ttk.Button(nav_frame, text="Forward", style="Primary.TButton", command=self.manage_option)
        self.forward_button.grid(row=0, column=1, padx=5)
