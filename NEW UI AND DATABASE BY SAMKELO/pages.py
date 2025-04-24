import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import cv2
import time
import os
import mysql.connector

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

class UserPage(tk.Frame):
    # Initialize the User Login Page
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#fafafa")
        self.controller = controller

        # Create header with title
        header = tk.Frame(self, bg="#4CAF50")
        header.pack(fill="x")
        tk.Label(header, text="Step 1: Technician Login", font=("Roboto", 14, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(pady=15)

        # Create content frame
        content = tk.Frame(self, bg="#f0f0f0", bd=1, relief="solid")
        content.pack(pady=10, padx=10, fill="both", expand=True)
        tk.Label(content, text="Please log in:", font=("Roboto", 12, "bold"), bg="#f0f0f0", fg="#212121").pack(pady=10)

        # User ID input
        tk.Label(content, text="User ID:", font=("Roboto", 11), bg="#f0f0f0", fg="#333333").pack(pady=5)
        user_id_entry = ttk.Entry(content, textvariable=self.controller.user_id_var, font=("Roboto", 11))
        user_id_entry.pack(pady=5, fill="x", padx=10)
        user_id_entry.focus_set()  # Set focus on User ID field

        # Password input
        tk.Label(content, text="Password:", font=("Roboto", 11), bg="#f0f0f0", fg="#333333").pack(pady=5)
        password_entry = ttk.Entry(content, textvariable=self.controller.password_var, font=("Roboto", 11), show="*")
        password_entry.pack(pady=5, fill="x", padx=10)

        # Navigation buttons
        nav_frame = tk.Frame(content, bg="#f0f0f0")
        nav_frame.pack(pady=10)
        back_btn = ttk.Button(nav_frame, text="Back", style="Secondary.TButton", command=lambda: self.controller.go_back("UserPage"))
        back_btn.pack(side="left", padx=5)
        next_btn = ttk.Button(nav_frame, text="Next", style="Primary.TButton", command=self.validate_and_proceed)
        next_btn.pack(side="left", padx=5)

    # Validate user credentials and proceed
    def validate_and_proceed(self):
        user_id = self.controller.user_id_var.get().strip()
        password = self.controller.password_var.get().strip()
        if not user_id or not password:
            messagebox.showerror("Missing Information", "Please enter both User ID and Password", parent=self.controller.root)
            return

        try:
            if self.controller.db_manager.authenticate_user(user_id, password):
                self.controller.show_frame("LocationPage")  # Proceed to next page
            else:
                messagebox.showerror("Authentication Failed", "Invalid User ID or Password", parent=self.controller.root)
                self.controller.password_var.set("")  # Clear password field
        except Exception as err:
            messagebox.showerror("Database Error", str(err), parent=self.controller.root)
            self.controller.password_var.set("")  # Clear password field

class LocationPage(tk.Frame):
    # Initialize the Location Selection Page
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#fafafa")
        self.controller = controller

        # Create header with title
        header = tk.Frame(self, bg="#4CAF50")
        header.pack(fill="x")
        tk.Label(header, text="Step 2: Location", font=("Roboto", 14, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(pady=15)

        # Create content frame
        content = tk.Frame(self, bg="#f0f0f0", bd=1, relief="solid")
        content.pack(pady=10, padx=10, fill="both", expand=True)
        tk.Label(content, text="Where are you?", font=("Roboto", 12, "bold"), bg="#f0f0f0", fg="#212121").pack(pady=10)
        # Location dropdown
        location_dropdown = ttk.Combobox(content, textvariable=self.controller.location_var, values=["New Battery Section", "Old Battery Section"], font=("Roboto", 11))
        location_dropdown.pack(pady=5, fill="x", padx=10)

        # Navigation buttons
        nav_frame = tk.Frame(content, bg="#f0f0f0")
        nav_frame.pack(pady=10)
        back_btn = ttk.Button(nav_frame, text="Back", style="Secondary.TButton", command=lambda: self.controller.go_back("LocationPage"))
        back_btn.pack(side="left", padx=5)
        next_btn = ttk.Button(nav_frame, text="Next", style="Primary.TButton", command=lambda: self.controller.validate_and_proceed("LocationPage", "ActivityPage", self.controller.location_var.get(), "Location selection"))
        next_btn.pack(side="left", padx=5)

class ActivityPage(tk.Frame):
    # Initialize the Action Selection Page
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#fafafa")
        self.controller = controller

        # Create header with title
        header = tk.Frame(self, bg="#4CAF50")
        header.pack(fill="x")
        tk.Label(header, text="Step 3: Action", font=("Roboto", 14, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(pady=15)

        # Create content frame
        content = tk.Frame(self, bg="#f0f0f0", bd=1, relief="solid")
        content.pack(pady=10, padx=10, fill="both", expand=True)
        tk.Label(content, text="What are you doing?", font=("Roboto", 12, "bold"), bg="#f0f0f0", fg="#212121").pack(pady=10)
        # Action dropdown
        activity_dropdown = ttk.Combobox(content, textvariable=self.controller.action_var, values=["Find", "Receive", "Ship", "Move"], font=("Roboto", 11))
        activity_dropdown.pack(pady=5, fill="x", padx=10)

        # Navigation buttons
        nav_frame = tk.Frame(content, bg="#f0f0f0")
        nav_frame.pack(pady=10)
        back_btn = ttk.Button(nav_frame, text="Back", style="Secondary.TButton", command=lambda: self.controller.go_back("ActivityPage"))
        back_btn.pack(side="left", padx=5)
        next_btn = ttk.Button(nav_frame, text="Next", style="Primary.TButton", command=lambda: self.controller.validate_and_proceed("ActivityPage", "ScanPage", self.controller.action_var.get(), "Action selection"))
        next_btn.pack(side="left", padx=5)

class ScanPage(tk.Frame):
    # Initialize the Barcode Entry Page
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#fafafa")
        self.controller = controller

        # Create header with title
        header = tk.Frame(self, bg="#4CAF50")
        header.pack(fill="x")
        tk.Label(header, text="Step 4: Enter Item Barcode", font=("Roboto", 14, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(pady=15)

        # Create content frame
        content = tk.Frame(self, bg="#f0f0f0", bd=1, relief="solid")
        content.pack(pady=10, padx=10, fill="both", expand=True)
        tk.Label(content, text="Enter the barcode:", font=("Roboto", 12, "bold"), bg="#f0f0f0", fg="#212121").pack(pady=10)

        # Barcode entry field
        self.barcode_entry = ttk.Entry(content, textvariable=self.controller.barcode_var, font=("Roboto", 11))
        self.barcode_entry.pack(pady=5, fill="x", padx=10)
        self.barcode_entry.focus_set()  # Set focus on barcode field
        # Bind Enter key to proceed
        self.barcode_entry.bind("<Return>", lambda e: self.controller.validate_and_proceed("ScanPage", "OperationSpecificPage", self.controller.barcode_var.get().strip(), "Barcode entry"))

        # Navigation buttons
        nav_frame = tk.Frame(content, bg="#f0f0f0")
        nav_frame.pack(pady=10)
        back_btn = ttk.Button(nav_frame, text="Back", style="Secondary.TButton", command=lambda: self.controller.go_back("ScanPage"))
        back_btn.pack(side="left", padx=5)
        next_btn = ttk.Button(nav_frame, text="Next", style="Primary.TButton", command=lambda: self.controller.validate_and_proceed("ScanPage", "OperationSpecificPage", self.controller.barcode_var.get().strip(), "Barcode entry"))
        next_btn.pack(side="left", padx=5)

    # Placeholder for camera stop (used in other pages)
    def stop_camera(self):
        pass

class OperationSpecificPage(tk.Frame):
    # Initialize the Operation Details Page
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#fafafa")
        self.controller = controller
        self.fields = []  # Store form fields
        self.widgets = []  # Store dynamic widgets

        # Create header with title
        header = tk.Frame(self, bg="#4CAF50")
        header.pack(fill="x")
        tk.Label(header, text="Step 5: Operation Details", font=("Roboto", 14, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(pady=15)

        # Create content frame
        self.content = tk.Frame(self, bg="#f0f0f0", bd=1, relief="solid")
        self.content.pack(pady=10, padx=10, fill="both", expand=True)

        # Navigation buttons
        self.nav_frame = tk.Frame(self.content, bg="#f0f0f0")
        self.nav_frame.pack(pady=10)
        back_btn = ttk.Button(self.nav_frame, text="Back", style="Secondary.TButton", command=lambda: self.controller.go_back("OperationSpecificPage"))
        back_btn.pack(side="left", padx=5)
        self.next_btn = ttk.Button(self.nav_frame, text="Next", style="Primary.TButton", command=self.validate_and_proceed)
        self.next_btn.pack(side="left", padx=5)

    # Load dynamic form fields based on operation
    def load_template(self):
        # Clear existing widgets except navigation
        for widget in self.content.winfo_children():
            if widget != self.nav_frame:
                widget.destroy()
        self.fields = []
        self.widgets = []

        operation = self.controller.action_var.get().strip()
        # Skip to PhotoPage if no fields for operation
        if operation not in self.controller.OPERATION_TEMPLATES or not self.controller.OPERATION_TEMPLATES[operation]["fields"]:
            self.controller.show_frame("PhotoPage")
            return

        # Display operation prompt
        tk.Label(self.content, text=f"Provide details for {operation}:", font=("Roboto", 12, "bold"), bg="#f0f0f0", fg="#212121").pack(pady=10)

        # Create form fields based on template
        for field in self.controller.OPERATION_TEMPLATES[operation]["fields"]:
            tk.Label(self.content, text=field["label"], font=("Roboto", 11), bg="#f0f0f0", fg="#333333").pack(pady=5)
            
            # Handle lookup fields (e.g., Find operation)
            if field.get("lookup"):
                barcode = self.controller.barcode_var.get().strip()
                try:
                    # Connect to database
                    conn = mysql.connector.connect(
                        host="127.0.0.1",
                        user="spiers_user",
                        password="spiers_pass",
                        database="spiers_system",
                        auth_plugin="mysql_native_password"
                    )
                    cursor = conn.cursor()
                    # Query latest operation for barcode
                    query = """
                        SELECT action, new_location, destination, source, battery_condition
                        FROM operations
                        WHERE barcode = %s
                        ORDER BY timestamp DESC
                        LIMIT 1
                    """
                    cursor.execute(query, (barcode,))
                    result = cursor.fetchone()
                    cursor.close()
                    conn.close()

                    # Determine location text
                    if result:
                        action, new_location, destination, source, battery_condition = result
                        if new_location:
                            location = new_location
                        elif action == "Ship":
                            location = f"Shipped to {destination}"
                        elif action == "Receive" and source == "Customer":
                            location = f"Received from Customer, Condition: {battery_condition}"
                        elif action == "Receive" and source == "Supplier":
                            location = "Received from Supplier"
                        else:
                            location = "Location not specified"
                    else:
                        location = "Item does not exist or has no recorded operations."
                except mysql.connector.Error as err:
                    location = f"Database error: {str(err)}"

                # Display location information
                location_label = tk.Label(self.content, text=location, font=("Roboto", 11), bg="#f0f0f0", fg="#333333")
                location_label.pack(pady=5, fill="x", padx=10)
                self.widgets.append(location_label)
            else:
                # Handle dropdown fields
                if field["type"] == "dropdown":
                    # Assign appropriate StringVar based on field variable
                    if field["variable"] == "new_location_var":
                        var = self.controller.new_location_var
                    elif field["variable"] == "battery_condition_var":
                        var = self.controller.battery_condition_var
                    elif field["variable"] == "destination_var":
                        var = self.controller.destination_var
                    elif field["variable"] == "source_var":
                        var = self.controller.source_var
                    elif field["variable"] == "customer_battery_condition_var":
                        var = self.controller.customer_battery_condition_var
                    else:
                        var = tk.StringVar()
                    # Create dropdown with options
                    dropdown = ttk.Combobox(self.content, textvariable=var, values=field["options"], font=("Roboto", 11))
                    dropdown.pack(pady=5, fill="x", padx=10)
                    self.fields.append((var, field["label"]))
                    self.widgets.append(dropdown)

                    # Bind conditional updates for Receive operation
                    if field.get("conditional") and operation == "Receive":
                        dropdown.bind("<<ComboboxSelected>>", lambda e: self.update_receive_fields())

        # Update fields for Receive operation if source is selected
        if operation == "Receive" and self.controller.source_var.get():
            self.update_receive_fields()

    # Update fields for Receive operation based on source
    def update_receive_fields(self):
        # Clear existing conditional widgets
        for widget in self.widgets:
            if hasattr(widget, "is_conditional") and widget.is_conditional:
                widget.destroy()
        self.widgets = [w for w in self.widgets if not (hasattr(w, "is_conditional") and w.is_conditional)]
        self.fields = [(var, label) for var, label in self.fields if label != "Battery Condition:"]

        source = self.controller.source_var.get().strip()
        if source == "Customer":
            # Add battery condition dropdown for customer source
            label = tk.Label(self.content, text="Battery Condition:", font=("Roboto", 11), bg="#f0f0f0", fg="#333333")
            label.pack(pady=5)
            label.is_conditional = True  # Mark as conditional
            dropdown = ttk.Combobox(self.content, textvariable=self.controller.customer_battery_condition_var, values=["Faulty", "Death-Row"], font=("Roboto", 11))
            dropdown.pack(pady=5, fill="x", padx=10)
            dropdown.is_conditional = True  # Mark as conditional
            self.widgets.extend([label, dropdown])
            self.fields.append((self.controller.customer_battery_condition_var, "Battery Condition:"))
            # Bind selection to update workflow message
            dropdown.bind("<<ComboboxSelected>>", lambda e: self.update_workflow_message())
        elif source == "Supplier":
            # Display workflow message for supplier source
            workflow = "Store and monitor its health."
            workflow_label = tk.Label(self.content, text=workflow, font=("Roboto", 11), bg="#f0f0f0", fg="#333333", wraplength=700)
            workflow_label.pack(pady=5, fill="x", padx=10)
            workflow_label.is_conditional = True  # Mark as conditional
            self.widgets.append(workflow_label)

        # Update workflow message if customer source and condition selected
        if source == "Customer" and self.controller.customer_battery_condition_var.get():
            self.update_workflow_message()

    # Update workflow message based on battery condition
    def update_workflow_message(self):
        # Clear existing workflow widgets
        for widget in self.widgets:
            if hasattr(widget, "is_workflow") and widget.is_workflow:
                widget.destroy()
        self.widgets = [w for w in self.widgets if not (hasattr(w, "is_workflow") and w.is_workflow)]

        condition = self.controller.customer_battery_condition_var.get().strip()
        if condition == "Faulty":
            workflow = "Diagnostic analysis, disassembly, repair, reassembly, testing, and recertification."
        elif condition == "Death-Row":
            workflow = "Take apart carefully, shred into tiny pieces, then into powder for use in making new batteries elsewhere."
        else:
            return  # No workflow message if condition not set

        # Display workflow message
        workflow_label = tk.Label(self.content, text=workflow, font=("Roboto", 11), bg="#f0f0f0", fg="#333333", wraplength=700)
        workflow_label.pack(pady=5, fill="x", padx=10)
        workflow_label.is_workflow = True  # Mark as workflow
        self.widgets.append(workflow_label)

    # Validate form fields and proceed
    def validate_and_proceed(self):
        # Check for empty required fields
        for var, label in self.fields:
            if not var.get().strip():
                messagebox.showerror("Missing Information", f"Please complete: {label}", parent=self.controller.root)
                return
        # Ensure battery condition is specified for customer source
        if self.controller.source_var.get() == "Customer" and not self.controller.customer_battery_condition_var.get().strip():
            messagebox.showerror("Missing Information", "Please specify the battery condition.", parent=self.controller.root)
            return
        self.controller.show_frame("PhotoPage")  # Proceed to photo capture

class PhotoPage(tk.Frame):
    # Initialize the Photo Capture Page
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#fafafa")
        self.controller = controller
        self.cap = None  # Camera capture object
        self.preview_running = False  # Camera preview status
        self.photo_path = None  # Path to captured photo

        # Create header with title
        header = tk.Frame(self, bg="#4CAF50")
        header.pack(fill="x")
        tk.Label(header, text="Step 6: Take Photo", font=("Roboto", 14, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(pady=15)

        # Create content frame
        content = tk.Frame(self, bg="#f0f0f0", bd=1, relief="solid")
        content.pack(pady=10, padx=10, fill="both", expand=True)
        tk.Label(content, text="Capture item photo:", font=("Roboto", 12, "bold"), bg="#f0f0f0", fg="#212121").pack(pady=10)

        # Camera preview label
        self.preview_label = tk.Label(content, bg="#f0f0f0")
        self.preview_label.pack(pady=10)

        # Capture and retake buttons
        btn_frame = tk.Frame(content, bg="#f0f0f0")
        btn_frame.pack(pady=10)
        self.capture_btn = ttk.Button(btn_frame, text="Capture", style="Primary.TButton", command=self.capture_photo)
        self.capture_btn.pack(side="left", padx=5)
        self.retake_btn = ttk.Button(btn_frame, text="Retake", style="Secondary.TButton", command=self.retake_photo, state="disabled")
        self.retake_btn.pack(side="left", padx=5)

        # Navigation buttons
        nav_frame = tk.Frame(content, bg="#f0f0f0")
        nav_frame.pack(pady=10)
        back_btn = ttk.Button(nav_frame, text="Back", style="Secondary.TButton", command=lambda: self.controller.go_back("PhotoPage"))
        back_btn.pack(side="left", padx=5)
        next_btn = ttk.Button(nav_frame, text="Next", style="Primary.TButton", command=lambda: self.controller.validate_and_proceed("PhotoPage", "ReactionPage", self.controller.photo_taken.get(), "Photo capture"))
        next_btn.pack(side="left", padx=5)

    # Start the camera for live preview
    def start_camera(self):
        self.stop_camera()  # Ensure any existing camera is stopped
        try:
            self.cap = cv2.VideoCapture(0)  # Initialize camera
            if not self.cap.isOpened():
                messagebox.showerror("Camera Error", "Failed to access camera. Please ensure the camera is connected and not in use.", parent=self.controller.root)
                self.cap = None
                return
        except Exception as e:
            messagebox.showerror("Camera Error", f"Error initializing camera: {str(e)}", parent=self.controller.root)
            self.cap = None
            return

        self.preview_running = True  # Enable preview
        self.update_preview()  # Start updating preview

    # Update camera preview frame
    def update_preview(self):
        if not self.preview_running or not self.cap:
            return

        try:
            ret, frame = self.cap.read()  # Read camera frame
            if ret:
                frame = cv2.resize(frame, (320, 240))  # Resize frame
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
                img = Image.fromarray(frame_rgb)
                imgtk = ImageTk.PhotoImage(image=img)
                self.preview_label.imgtk = imgtk  # Keep reference
                self.preview_label.configure(image=imgtk)
            else:
                messagebox.showwarning("Camera Warning", "Failed to read frame from camera.", parent=self.controller.root)
                self.stop_camera()
                return
        except Exception as e:
            messagebox.showerror("Preview Error", f"Error updating preview: {str(e)}", parent=self.controller.root)
            self.stop_camera()
            return

        self.after(10, self.update_preview)  # Schedule next update

    # Capture a photo from the camera
    def capture_photo(self):
        if not self.cap or not self.cap.isOpened():
            messagebox.showerror("Camera Error", "Camera is not available. Please restart the application.", parent=self.controller.root)
            return

        try:
            ret, frame = self.cap.read()  # Read frame
            if ret:
                timestamp = time.strftime("%Y%m%d_%H%M%S")  # Generate timestamp
                self.photo_path = f"photo_{timestamp}.jpg"  # Set photo filename
                if not os.access(".", os.W_OK):
                    messagebox.showerror("Storage Error", "No write permission in the current directory.", parent=self.controller.root)
                    return
                cv2.imwrite(self.photo_path, frame)  # Save photo
                self.controller.photo_taken.set(True)  # Mark photo as taken
                self.capture_btn.configure(state="disabled")  # Disable capture button
                self.retake_btn.configure(state="normal")  # Enable retake button
                messagebox.showinfo("Photo Captured", f"Photo saved as {self.photo_path}", parent=self.controller.root)
            else:
                messagebox.showerror("Capture Error", "Failed to capture photo.", parent=self.controller.root)
        except Exception as e:
            messagebox.showerror("Capture Error", f"Error saving photo: {str(e)}", parent=self.controller.root)

    # Retake a photo by deleting the previous one
    def retake_photo(self):
        if self.photo_path and os.path.exists(self.photo_path):
            try:
                os.remove(self.photo_path)  # Delete existing photo
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete photo: {str(e)}", parent=self.controller.root)
        self.controller.photo_taken.set(False)  # Reset photo taken flag
        self.capture_btn.configure(state="normal")  # Enable capture button
        self.retake_btn.configure(state="disabled")  # Disable retake button
        self.start_camera()  # Restart camera

    # Stop the camera and clear preview
    def stop_camera(self):
        self.preview_running = False  # Stop preview updates
        if self.cap:
            try:
                self.cap.release()  # Release camera
            except Exception as e:
                print(f"Error releasing camera: {str(e)}")
            self.cap = None
        self.preview_label.configure(image="")  # Clear preview

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

class ConfirmationPage(tk.Frame):
    # Initialize the Confirmation Page
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#fafafa")
        self.controller = controller

        # Create header with title
        header = tk.Frame(self, bg="#4CAF50")
        header.pack(fill="x")
        tk.Label(header, text="Step 8: Confirm Details", font=("Roboto", 14, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(pady=15)

        # Create content frame
        content = tk.Frame(self, bg="#f0f0f0", bd=1, relief="solid")
        content.pack(pady=10, padx=10, fill="both", expand=True)
        tk.Label(content, text="Review your submission:", font=("Roboto", 12, "bold"), bg="#f0f0f0", fg="#212121").pack(pady=10)

        # Display technician ID
        tk.Label(content, text="Technician ID:", font=("Roboto", 11, "bold"), bg="#f0f0f0", fg="#212121", anchor="w").pack(fill="x", padx=10)
        tk.Label(content, text=self.controller.user_id_var.get() or "N/A", font=("Roboto", 11), bg="#f0f0f0", fg="#333333", anchor="w").pack(fill="x", padx=10)

        # Display location
        tk.Label(content, text="Location:", font=("Roboto", 11, "bold"), bg="#f0f0f0", fg="#212121", anchor="w").pack(fill="x", padx=10)
        tk.Label(content, text=self.controller.location_var.get() or "N/A", font=("Roboto", 11), bg="#f0f0f0", fg="#333333", anchor="w").pack(fill="x", padx=10)

        # Display action
        tk.Label(content, text="Action:", font=("Roboto", 11, "bold"), bg="#f0f0f0", fg="#212121", anchor="w").pack(fill="x", padx=10)
        tk.Label(content, text=self.controller.action_var.get() or "N/A", font=("Roboto", 11), bg="#f0f0f0", fg="#333333", anchor="w").pack(fill="x", padx=10)

        # Display barcode
        tk.Label(content, text="Barcode:", font=("Roboto", 11, "bold"), bg="#f0f0f0", fg="#212121", anchor="w").pack(fill="x", padx=10)
        tk.Label(content, text=self.controller.barcode_var.get() or "N/A", font=("Roboto", 11), bg="#f0f0f0", fg="#333333", anchor="w").pack(fill="x", padx=10)

        # Display operation-specific fields
        operation = self.controller.action_var.get().strip()
        if operation in self.controller.OPERATION_TEMPLATES and self.controller.OPERATION_TEMPLATES[operation]["fields"]:
            for field in self.controller.OPERATION_TEMPLATES[operation]["fields"]:
                if field.get("lookup"):
                    continue  # Skip lookup fields
                tk.Label(content, text=field["label"], font=("Roboto", 11, "bold"), bg="#f0f0f0", fg="#212121", anchor="w").pack(fill="x", padx=10)
                # Retrieve field value based on variable name
                if field["variable"] == "new_location_var":
                    value = self.controller.new_location_var.get()
                elif field["variable"] == "battery_condition_var":
                    value = self.controller.battery_condition_var.get()
                elif field["variable"] == "destination_var":
                    value = self.controller.destination_var.get()
                elif field["variable"] == "source_var":
                    value = self.controller.source_var.get()
                else:
                    value = "N/A"
                tk.Label(content, text=value or "N/A", font=("Roboto", 11), bg="#f0f0f0", fg="#333333", anchor="w").pack(fill="x", padx=10)

        # Display battery condition for customer source
        if operation == "Receive" and self.controller.source_var.get() == "Customer":
            tk.Label(content, text="Battery Condition:", font=("Roboto", 11, "bold"), bg="#f0f0f0", fg="#212121", anchor="w").pack(fill="x", padx=10)
            tk.Label(content, text=self.controller.customer_battery_condition_var.get() or "N/A", font=("Roboto", 11), bg="#f0f0f0", fg="#333333", anchor="w").pack(fill="x", padx=10)

        # Display photo path
        tk.Label(content, text="Photo Path:", font=("Roboto", 11, "bold"), bg="#f0f0f0", fg="#212121", anchor="w").pack(fill="x", padx=10)
        photo_path = self.controller.frames["PhotoPage"].photo_path if self.controller.frames["PhotoPage"].photo_path else "N/A"
        tk.Label(content, text=photo_path, font=("Roboto", 11), bg="#f0f0f0", fg="#333333", anchor="w").pack(fill="x", padx=10)

        # Display reaction sentence
        tk.Label(content, text="Reaction:", font=("Roboto", 11, "bold"), bg="#f0f0f0", fg="#212121", anchor="w").pack(fill="x", padx=10)
        reaction = f"I feel {self.controller.adjective_var.get()} about {self.controller.action_var.get()} because it’s {self.controller.reason_var.get()}." if self.controller.adjective_var.get() and self.controller.reason_var.get() else "N/A"
        tk.Label(content, text=reaction, font=("Roboto", 11), bg="#f0f0f0", fg="#666666", anchor="w", wraplength=700).pack(fill="x", padx=10)

        # Navigation buttons
        nav_frame = tk.Frame(content, bg="#f0f0f0")
        nav_frame.pack(pady=10)
        back_btn = ttk.Button(nav_frame, text="Back", style="Secondary.TButton", command=lambda: self.controller.go_back("ConfirmationPage"))
        back_btn.pack(side="left", padx=5)
        next_btn = ttk.Button(nav_frame, text="Next", style="Primary.TButton", command=lambda: self.controller.show_frame("DonePage"))
        next_btn.pack(side="left", padx=5)

class DonePage(tk.Frame):
    # Initialize the Done Page
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#fafafa")
        self.controller = controller
        self.operation_id = None  # Store operation ID

        # Create header with title
        header = tk.Frame(self, bg="#4CAF50")
        header.pack(fill="x")
        tk.Label(header, text="Step 9: Done", font=("Roboto", 14, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(pady=15)

        # Create content frame
        content = tk.Frame(self, bg="#f0f0f0", bd=1, relief="solid")
        content.pack(pady=10, padx=10, fill="both", expand=True)

        # Display completion message
        tk.Label(content, text="SPIERS System", font=("Roboto", 16, "bold"), bg="#f0f0f0", fg="#212121").pack(pady=10)
        tk.Label(content, text="Thank you!\nOperation logged.", font=("Roboto", 11), bg="#f0f0f0", fg="#333333").pack(pady=10)

        # Display operation summary
        tk.Label(content, text="Operation Summary:", font=("Roboto", 12, "bold"), bg="#f0f0f0", fg="#212121").pack(pady=5)
        self.summary_text = tk.Text(content, height=8, width=50, font=("Roboto", 11), bg="#f0f0f0", fg="#333333", wrap="word")
        self.summary_text.pack(pady=5, padx=10)
        self.summary_text.config(state="disabled")  # Make summary read-only

        # Next action prompt
        tk.Label(content, text="Next?", font=("Roboto", 12, "bold"), bg="#f0f0f0", fg="#212121").pack(pady=10)
        btn_frame = tk.Frame(content, bg="#f0f0f0")
        btn_frame.pack(pady=10)
        save_btn = ttk.Button(btn_frame, text="Save Summary", style="Primary.TButton", command=self.save_summary)
        save_btn.pack(side="left", padx=5)
        new_op_btn = ttk.Button(btn_frame, text="New Op", style="Primary.TButton", command=self.start_new_operation)
        new_op_btn.pack(side="left", padx=5)
        exit_btn = ttk.Button(btn_frame, text="Exit", style="Exit.TButton", command=self.controller.root.destroy)
        exit_btn.pack(side="left", padx=5)

    # Override tkraise to log operation and display summary
    def tkraise(self, *args, **kwargs):
        # Prepare operation data for logging
        operation_data = {
            "technician_id": self.controller.user_id_var.get(),
            "location": self.controller.location_var.get(),
            "action": self.controller.action_var.get(),
            "barcode": self.controller.barcode_var.get(),
            "new_location": self.controller.new_location_var.get(),
            "source": self.controller.source_var.get(),
            "destination": self.controller.destination_var.get(),
            "battery_condition": self.controller.customer_battery_condition_var.get(),
            "photo_path": self.controller.frames["PhotoPage"].photo_path,
            "reaction": f"I feel {self.controller.adjective_var.get()} about {self.controller.action_var.get()} because it’s {self.controller.reason_var.get()}." if self.controller.adjective_var.get() and self.controller.reason_var.get() else None
        }
        try:
            # Log operation to database
            self.operation_id = self.controller.db_manager.log_operation(operation_data)
            if self.operation_id:
                # Generate and display operation summary
                summary = self.controller.db_manager.generate_operation_summary(self.operation_id)
                self.summary_text.config(state="normal")
                self.summary_text.delete("1.0", tk.END)
                self.summary_text.insert(tk.END, summary)
                self.summary_text.config(state="disabled")
        except Exception as err:
            messagebox.showerror("Database Error", str(err), parent=self.controller.root)
        super().tkraise(*args, **kwargs)  # Call parent tkraise

    # Save operation summary to a file
    def save_summary(self):
        if not self.operation_id:
            messagebox.showerror("Error", "No operation to summarize.", parent=self.controller.root)
            return
        summary = self.controller.db_manager.generate_operation_summary(self.operation_id)
        timestamp = time.strftime("%Y%m%d_%H%M%S")  # Generate timestamp
        filename = f"operation_summary_{self.operation_id}_{timestamp}.txt"  # Set filename
        try:
            with open(filename, "w") as f:
                f.write(summary)  # Write summary to file
            messagebox.showinfo("Success", f"Summary saved as {filename}", parent=self.controller.root)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save summary: {str(e)}", parent=self.controller.root)

    # Start a new operation
    def start_new_operation(self):
        self.controller.reset_variables()  # Reset all input variables
        self.operation_id = None  # Clear operation ID
        self.summary_text.config(state="normal")
        self.summary_text.delete("1.0", tk.END)  # Clear summary
        self.summary_text.config(state="disabled")
        self.controller.show_frame("StartPage")  # Return to start page
