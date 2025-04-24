import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class StartPage(tk.Frame):
    # Initialize the Start Page
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#fafafa")  # Set background color
        self.controller = controller  # Reference to the main app controller

        # Create header with title
        header = tk.Frame(self, bg="#4CAF50")
        header.pack(fill="x")
        tk.Label(header, text="SPIERS Smart System", font=("Roboto", 16, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(pady=15)

        # Create content frame
        content = tk.Frame(self, bg="#f0f0f0", bd=1, relief="solid")
        content.pack(pady=10, padx=10, fill="both", expand=True)
        # Start session button
        start_btn = ttk.Button(content, text="Start Session", style="Primary.TButton", command=lambda: self.controller.show_frame("UserPage"))
        start_btn.pack(pady=10)

        # Attempt to load and display logo
        try:
            logo_img = Image.open("logo.jpg")
            logo_img = logo_img.resize((300, int(300 * logo_img.height / logo_img.width)), Image.LANCZOS)  # Resize logo
            logo_image = ImageTk.PhotoImage(logo_img)
            logo_label = tk.Label(content, image=logo_image, bg="#f0f0f0")
            logo_label.image = logo_image  # Keep reference to avoid garbage collection
            logo_label.pack(pady=10)
        except Exception as e:
            print(f"Error loading logo image: {e}")  # Log error
            tk.Label(content, text="[Logo Failed to Load]", font=("Roboto", 11), bg="#f0f0f0", fg="red").pack(pady=10)
