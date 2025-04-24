import tkinter as tk
from tkinter import ttk, messagebox

class SpiersApp:
    # Define operation templates for dynamic form generation
    OPERATION_TEMPLATES = {
        "Move": {
            "fields": [
                {"label": "New Location:", "type": "dropdown", "variable": "new_location_var", "options": ["New Battery Section", "Old Battery Section"]}
            ]
        },
        "Receive": {
            "fields": [
                {"label": "Source:", "type": "dropdown", "variable": "source_var", "options": ["Customer", "Supplier"], "conditional": True},
                {"label": "Store in Location:", "type": "dropdown", "variable": "new_location_var", "options": ["New Battery Section", "Old Battery Section"]}
            ]
        },
        "Ship": {
            "fields": [
                {"label": "Destination:", "type": "dropdown", "variable": "destination_var", "options": ["Dealership A", "Dealership B"]}
            ]
        },
        "Find": {
            "fields": [
                {"label": "Battery Location:", "type": "label", "lookup": True}
            ]
        }
    }

    # Initialize the main application
    def __init__(self, root, page_classes, db_manager):
        self.root = root  # Main Tkinter window
        self.root.title("SPIERS Smart System")  # Set window title
        self.root.geometry("800x480")  # Set window size
        self.root.configure(bg="#fafafa")  # Set background color
        self.root.minsize(400, 300)  # Set minimum window size

        # Initialize database manager
        self.db_manager = db_manager

        # Initialize Tkinter variables for form inputs
        self.user_id_var = tk.StringVar()  # User ID input
        self.password_var = tk.StringVar()  # Password input
        self.location_var = tk.StringVar()  # Location input
        self.action_var = tk.StringVar()  # Action input
        self.barcode_var = tk.StringVar()  # Barcode input
        self.new_location_var = tk.StringVar()  # New location input
        self.battery_condition_var = tk.StringVar()  # Battery condition input
        self.destination_var = tk.StringVar()  # Destination input
        self.source_var = tk.StringVar()  # Source input
        self.customer_battery_condition_var = tk.StringVar()  # Customer battery condition input
        self.adjective_var = tk.StringVar()  # Adjective input
        self.reason_var = tk.StringVar()  # Reason input
        self.photo_taken = tk.BooleanVar(value=False)  # Photo taken flag

        # Configure Tkinter styles for UI elements
        self.style = ttk.Style()
        self.style.theme_use("clam")  # Use 'clam' theme for consistent look
        self.style.configure("TButton", font=("Roboto", 11), padding=10)  # Default button style
        self.style.configure("Primary.TButton", background="#4CAF50", foreground="#FFFFFF")  # Primary button style
        self.style.configure("Secondary.TButton", background="#D32F2F", foreground="#FFFFFF")  # Secondary button style
        self.style.configure("Exit.TButton", background="#D32F2F", foreground="#FFFFFF")  # Exit button style
        self.style.map("Primary.TButton", background=[("active", "#388E3C")])  # Primary button hover effect
        self.style.map("Secondary.TButton", background=[("active", "#B71C1C")])  # Secondary button hover effect
        self.style.map("Exit.TButton", background=[("active", "#B71C1C")])  # Exit button hover effect
        self.style.configure("TCombobox", font=("Roboto", 11))  # Combobox style

        # Create main container for pages
        self.container = tk.Frame(self.root, bg="#fafafa")
        self.container.pack(fill="both", expand=True)  # Fill available space
        self.container.grid_rowconfigure(0, weight=1)  # Configure row to expand
        self.container.grid_columnconfigure(0, weight=1)  # Configure column to expand

        # Initialize page frames
        self.frames = {}
        self.page_classes = page_classes
        for page_name, page_class in self.page_classes.items():
            frame = page_class(self.container, self)  # Create page instance
            self.frames[page_name] = frame  # Store page in frames dictionary
            frame.grid(row=0, column=0, sticky="nsew")  # Place page in grid

        # Show the initial start page
        self.show_frame("StartPage")

    # Display a specific page
    def show_frame(self, page_name):
        if page_name in self.frames:
            # Stop camera if switching away from PhotoPage
            if "PhotoPage" in self.frames and self.frames["PhotoPage"] != self.frames[page_name]:
                self.frames["PhotoPage"].stop_camera()
            self.frames[page_name].tkraise()  # Bring the page to the front
            # Load template for OperationSpecificPage
            if page_name == "OperationSpecificPage":
                self.frames["OperationSpecificPage"].load_template()
            # Start camera for PhotoPage
            elif page_name == "PhotoPage":
                self.frames["PhotoPage"].start_camera()

    # Navigate to the previous page in the sequence
    def go_back(self, current_page):
        # Define the page navigation sequence
        page_sequence = ["StartPage", "UserPage", "LocationPage", "ActivityPage", "ScanPage", "OperationSpecificPage", "PhotoPage", "ReactionPage", "ConfirmationPage", "DonePage"]
        current_index = page_sequence.index(current_page)  # Get current page index
        if current_index > 0:
            self.show_frame(page_sequence[current_index - 1])  # Show previous page

    # Validate input and proceed to the next page
    def validate_and_proceed(self, current_page, next_page, validation_field, field_name):
        # Check if validation field is a boolean
        if isinstance(validation_field, bool):
            if not validation_field:
                messagebox.showerror("Missing Information", f"Please complete: {field_name}", parent=self.root)
                return
        # Check if validation field is a non-empty string
        elif not validation_field.strip():
            messagebox.showerror("Missing Information", f"Please complete: {field_name}", parent=self.root)
            return
        self.show_frame(next_page)  # Proceed to the next page

    # Reset all Tkinter variables to their default values
    def reset_variables(self):
        self.user_id_var.set("")  # Clear user ID
        self.password_var.set("")  # Clear password
        self.location_var.set("")  # Clear location
        self.action_var.set("")  # Clear action
        self.barcode_var.set("")  # Clear barcode
        self.new_location_var.set("")  # Clear new location
        self.battery_condition_var.set("")  # Clear battery condition
        self.destination_var.set("")  # Clear destination
        self.source_var.set("")  # Clear source
        self.customer_battery_condition_var.set("")  # Clear customer battery condition
        self.photo_taken.set(False)  # Reset photo taken flag
        self.adjective_var.set("")  # Clear adjective
        self.reason_var.set("")  # Clear reason
