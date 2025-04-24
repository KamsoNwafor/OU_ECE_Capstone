import tkinter as tk
from tkinter import ttk, messagebox

class ReactionPage(tk.Frame):
    # Initialize the Reaction Input Page
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#fafafa")
        self.controller = controller

        # Create header with title
        header = tk.Frame(self, bg="#4CAF50")
        header.pack(fill="x")
        tk.Label(header, text="Step 7: How Are You Feeling?", font=("Roboto", 14, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(pady=15)

        # Create content frame
        content = tk.Frame(self, bg="#f0f0f0", bd=1, relief="solid")
        content.pack(pady=10, padx=10, fill="both", expand=True)
        tk.Label(content, text="Share your feelings about the activity:", font=("Roboto", 12, "bold"), bg="#f0f0f0", fg="#212121").pack(pady=10)

        # Adjective input
        tk.Label(content, text="I feel:", font=("Roboto", 11), bg="#f0f0f0", fg="#333333").pack(pady=5)
        adjective_dropdown = ttk.Combobox(content, textvariable=self.controller.adjective_var, values=["Excited", "Tired", "Confident", "Frustrated", "Happy", "Bored"], font=("Roboto", 11))
        adjective_dropdown.pack(pady=5, fill="x", padx=10)

        # Reason input
        tk.Label(content, text="Because it’s:", font=("Roboto", 11), bg="#f0f0f0", fg="#333333").pack(pady=5)
        reason_dropdown = ttk.Combobox(content, textvariable=self.controller.reason_var, values=["challenging", "routine", "rewarding", "stressful", "fun", "tedious"], font=("Roboto", 11))
        reason_dropdown.pack(pady=5, fill="x", padx=10)

        # Madlib sentence display
        self.madlib_label = tk.Label(content, text="", font=("Roboto", 11), bg="#f0f0f0", fg="#666666", wraplength=700)
        self.madlib_label.pack(pady=10)

        # Bind dropdowns to update madlib sentence
        adjective_dropdown.bind("<<ComboboxSelected>>", lambda e: self.update_madlib())
        reason_dropdown.bind("<<ComboboxSelected>>", lambda e: self.update_madlib())

        # Navigation buttons
        nav_frame = tk.Frame(content, bg="#f0f0f0")
        nav_frame.pack(pady=10)
        back_btn = ttk.Button(nav_frame, text="Back", style="Secondary.TButton", command=lambda: self.controller.go_back("ReactionPage"))
        back_btn.pack(side="left", padx=5)
        next_btn = ttk.Button(nav_frame, text="Next", style="Primary.TButton", command=self.validate_and_proceed)
        next_btn.pack(side="left", padx=5)

    # Update the madlib sentence based on selections
    def update_madlib(self):
        adjective = self.controller.adjective_var.get().strip()
        reason = self.controller.reason_var.get().strip()
        activity = self.controller.action_var.get().strip()
        if adjective and reason and activity:
            sentence = f"I feel {adjective} about {activity} because it’s {reason}."  # Create sentence
            self.madlib_label.configure(text=sentence)
        else:
            self.madlib_label.configure(text="")  # Clear if incomplete

    # Validate reaction inputs and proceed
    def validate_and_proceed(self):
        if not self.controller.adjective_var.get().strip():
            messagebox.showerror("Missing Information", "Please select how you feel", parent=self.controller.root)
            return
        if not self.controller.reason_var.get().strip():
            messagebox.showerror("Missing Information", "Please select a reason", parent=self.controller.root)
            return
        messagebox.showinfo("Reaction Recorded", "Your reaction has been recorded!", parent=self.controller.root)
        self.controller.show_frame("ConfirmationPage")  # Proceed to confirmation
