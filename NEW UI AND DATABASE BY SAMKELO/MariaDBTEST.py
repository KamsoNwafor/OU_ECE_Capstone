import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import cv2
import time
import os
import mysql.connector  # For MariaDB connectivity
import hashlib  # For password hashing (fallback)

# Initialize MariaDB database (verify connection)
def init_db():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="spiers_user",
            password="spiers_pass",
            database="spiers_system",
            auth_plugin="mysql_native_password"
        )
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        raise

# Call init_db to verify connection when the application starts
init_db()

# Initialize main window
root = tk.Tk()
root.title("SPIERS Smart System")
root.geometry("800x480")
root.configure(bg="#fafafa")
root.minsize(400, 300)

# Create Tkinter variables
user_id_var = tk.StringVar()
password_var = tk.StringVar()
location_var = tk.StringVar()
action_var = tk.StringVar()
barcode_var = tk.StringVar()
new_location_var = tk.StringVar()
battery_condition_var = tk.StringVar()
destination_var = tk.StringVar()
source_var = tk.StringVar()
customer_battery_condition_var = tk.StringVar()
adjective_var = tk.StringVar()
reason_var = tk.StringVar()
photo_taken = tk.BooleanVar(value=False)

# Mock database for name locations (for Find operation)
BATTERY_LOCATIONS = {
    "12345": "New Battery Section",
    "67890": "Old Battery Section",
}

# Define operation-specific templates
OPERATION_TEMPLATES = {
    "Move": {
        "fields": [
            {
                "label": "New Location:",
                "type": "dropdown",
                "variable": "new_location_var",
                "options": ["New Battery Section", "Old Battery Section"]
            }
        ]
    },
    "Receive": {
        "fields": [
            {
                "label": "Source:",
                "type": "dropdown",
                "variable": "source_var",
                "options": ["Customer", "Supplier"],
                "conditional": True
            }
        ]
    },
    "Ship": {
        "fields": [
            {
                "label": "Destination:",
                "type": "dropdown",
                "variable": "destination_var",
                "options": ["Dealership A", "Dealership B"]
            }
        ]
    },
    "Find": {
        "fields": [
            {
                "label": "Battery Location:",
                "type": "label",
                "lookup": True
            }
        ]
    }
}

# Define styles
style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("Roboto", 11), padding=10)
style.configure("Primary.TButton", background="#4CAF50", foreground="#FFFFFF")
style.configure("Secondary.TButton", background="#D32F2F", foreground="#FFFFFF")
style.configure("Exit.TButton", background="#D32F2F", foreground="#FFFFFF")
style.map("Primary.TButton", background=[("active", "#388E3C")])
style.map("Secondary.TButton", background=[("active", "#B71C1C")])
style.map("Exit.TButton", background=[("active", "#B71C1C")])
style.configure("TCombobox", font=("Roboto", 11))

# Function to show a specific frame
def show_frame(frame):
    if "PhotoPage" in frames and frames["PhotoPage"] != frame:
        frames["PhotoPage"].stop_camera()
    frame.tkraise()
    if frame == frames["OperationSpecificPage"]:
        frames["OperationSpecificPage"].load_template()
    elif frame == frames["PhotoPage"]:
        frames["PhotoPage"].start_camera()

# Navigation function to go back
def go_back(current_frame):
    if current_frame == frames["UserPage"]:
        show_frame(frames["StartPage"])
    elif current_frame == frames["LocationPage"]:
        show_frame(frames["UserPage"])
    elif current_frame == frames["ActivityPage"]:
        show_frame(frames["LocationPage"])
    elif current_frame == frames["ScanPage"]:
        show_frame(frames["ActivityPage"])
    elif current_frame == frames["OperationSpecificPage"]:
        show_frame(frames["ScanPage"])
    elif current_frame == frames["PhotoPage"]:
        show_frame(frames["OperationSpecificPage"])
    elif current_frame == frames["ReactionPage"]:
        show_frame(frames["PhotoPage"])
    elif current_frame == frames["ConfirmationPage"]:
        show_frame(frames["ReactionPage"])
    elif current_frame == frames["DonePage"]:
        show_frame(frames["ConfirmationPage"])

# Validation function
def validate_step(field_value, field_name, current_frame, next_frame):
    if isinstance(field_value, bool):
        if not field_value:
            messagebox.showerror("Missing Information", f"Please complete: {field_name}", parent=root)
            show_frame(current_frame)
            return False
    elif not field_value.strip():
        messagebox.showerror("Missing Information", f"Please complete: {field_name}", parent=root)
        show_frame(current_frame)
        return False
    return True

# Navigation function to go next
def go_next(current_frame, next_frame, validation_field, field_name):
    if validate_step(validation_field, field_name, current_frame, next_frame):
        show_frame(next_frame)

# Function to reset all variables
def reset_variables():
    user_id_var.set("")
    password_var.set("")
    location_var.set("")
    action_var.set("")
    barcode_var.set("")
    new_location_var.set("")
    battery_condition_var.set("")
    destination_var.set("")
    source_var.set("")
    customer_battery_condition_var.set("")
    photo_taken.set(False)
    adjective_var.set("")
    reason_var.set("")

# Function to log operation to MariaDB
def log_operation():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="spiers_user",
            password="spiers_pass",
            database="spiers_system",
            auth_plugin="mysql_native_password"
        )
        cursor = conn.cursor()

        # Prepare the operation data
        operation = action_var.get().strip()
        reaction = f"I feel {adjective_var.get()} about {action_var.get()} because it’s {reason_var.get()}." if adjective_var.get() and reason_var.get() else None
        photo_path = frames["PhotoPage"].photo_path if frames["PhotoPage"].photo_path else None

        # Insert into operations table
        query = """
            INSERT INTO operations (technician_id, location, action, barcode, new_location, source, destination, battery_condition, photo_path, reaction)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            user_id_var.get(),
            location_var.get(),
            action_var.get(),
            barcode_var.get(),
            new_location_var.get() or None,
            source_var.get() or None,
            destination_var.get() or None,
            customer_battery_condition_var.get() or None,
            photo_path,
            reaction
        )
        cursor.execute(query, values)
        conn.commit()

        # Get the operation_id of the newly inserted operation
        cursor.execute("SELECT LAST_INSERT_ID()")
        operation_id = cursor.fetchone()[0]

        cursor.close()
        conn.close()
        return operation_id
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error logging operation: {str(err)}", parent=root)
        return None

# Function to generate operation summary
def generate_operation_summary(operation_id):
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="spiers_user",
            password="spiers_pass",
            database="spiers_system",
            auth_plugin="mysql_native_password"
        )
        cursor = conn.cursor()

        # Query the operation details
        query = "SELECT * FROM operations WHERE operation_id = %s"
        cursor.execute(query, (operation_id,))
        operation = cursor.fetchone()

        if not operation:
            cursor.close()
            conn.close()
            return "Operation not found."

        # Unpack the operation data
        (op_id, tech_id, loc, action, barcode, new_loc, src, dest, batt_cond, photo_path, reaction, timestamp) = operation

        # Build the summary
        summary = f"Operation Summary (ID: {op_id})\n"
        summary += f"Timestamp: {timestamp}\n"
        summary += f"Technician ID: {tech_id}\n"
        summary += f"Location: {loc}\n"
        summary += f"Action: {action}\n"
        summary += f"Barcode: {barcode}\n"
        
        if action == "Move" and new_loc:
            summary += f"New Location: {new_loc}\n"
        elif action == "Receive":
            summary += f"Source: {src}\n"
            if src == "Customer" and batt_cond:
                summary += f"Battery Condition: {batt_cond}\n"
        elif action == "Ship" and dest:
            summary += f"Destination: {dest}\n"
        elif action == "Find":
            summary += f"Battery Location: {BATTERY_LOCATIONS.get(barcode, 'Item does not exist.')}\n"

        summary += f"Photo Path: {photo_path if photo_path else 'N/A'}\n"
        summary += f"Reaction: {reaction if reaction else 'N/A'}\n"

        cursor.close()
        conn.close()
        return summary
    except mysql.connector.Error as err:
        return f"Error generating summary: {str(err)}"

# OperationSpecificPage
class OperationSpecificPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#fafafa")
        self.controller = controller
        self.fields = []
        self.widgets = []

        # Header
        header = tk.Frame(self, bg="#4CAF50")
        header.pack(fill="x")
        tk.Label(header, text="Step 5: Operation Details", font=("Roboto", 14, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(pady=15)

        # Content
        self.content = tk.Frame(self, bg="#f0f0f0", bd=1, relief="solid")
        self.content.pack(pady=10, padx=10, fill="both", expand=True)

        # Navigation
        self.nav_frame = tk.Frame(self.content, bg="#f0f0f0")
        self.nav_frame.pack(pady=10)
        back_btn = ttk.Button(self.nav_frame, text="Back", style="Secondary.TButton", command=lambda: go_back(self))
        back_btn.pack(side="left", padx=5)
        self.next_btn = ttk.Button(self.nav_frame, text="Next", style="Primary.TButton", command=self.validate_and_proceed)
        self.next_btn.pack(side="left", padx=5)

    def load_template(self):
        # Clear previous content (except navigation)
        for widget in self.content.winfo_children():
            if widget != self.nav_frame:
                widget.destroy()
        self.fields = []
        self.widgets = []

        operation = action_var.get().strip()
        if operation not in OPERATION_TEMPLATES or not OPERATION_TEMPLATES[operation]["fields"]:
            show_frame(frames["PhotoPage"])
            return

        tk.Label(self.content, text=f"Provide details for {operation}:", font=("Roboto", 12, "bold"), bg="#f0f0f0", fg="#212121").pack(pady=10)

        for field in OPERATION_TEMPLATES[operation]["fields"]:
            tk.Label(self.content, text=field["label"], font=("Roboto", 11), bg="#f0f0f0", fg="#333333").pack(pady=5)
            
            if field.get("lookup"):
                barcode = barcode_var.get().strip()
                location = BATTERY_LOCATIONS.get(barcode, "Item does not exist.")
                location_label = tk.Label(self.content, text=location, font=("Roboto", 11), bg="#f0f0f0", fg="#333333")
                location_label.pack(pady=5, fill="x", padx=10)
                self.widgets.append(location_label)
            else:
                if field["type"] == "dropdown":
                    if field["variable"] == "new_location_var":
                        var = new_location_var
                    elif field["variable"] == "battery_condition_var":
                        var = battery_condition_var
                    elif field["variable"] == "destination_var":
                        var = destination_var
                    elif field["variable"] == "source_var":
                        var = source_var
                    elif field["variable"] == "customer_battery_condition_var":
                        var = customer_battery_condition_var
                    else:
                        var = tk.StringVar()
                    dropdown = ttk.Combobox(self.content, textvariable=var, values=field["options"], font=("Roboto", 11))
                    dropdown.pack(pady=5, fill="x", padx=10)
                    self.fields.append((var, field["label"]))
                    self.widgets.append(dropdown)

                    if field.get("conditional") and operation == "Receive":
                        dropdown.bind("<<ComboboxSelected>>", lambda e: self.update_receive_fields())

        if operation == "Receive" and source_var.get():
            self.update_receive_fields()

    def update_receive_fields(self):
        for widget in self.widgets:
            if hasattr(widget, "is_conditional") and widget.is_conditional:
                widget.destroy()
        self.widgets = [w for w in self.widgets if not (hasattr(w, "is_conditional") and w.is_conditional)]
        self.fields = [(var, label) for var, label in self.fields if label != "Battery Condition:"]

        source = source_var.get().strip()
        if source == "Customer":
            label = tk.Label(self.content, text="Battery Condition:", font=("Roboto", 11), bg="#f0f0f0", fg="#333333")
            label.pack(pady=5)
            label.is_conditional = True
            dropdown = ttk.Combobox(self.content, textvariable=customer_battery_condition_var, values=["Faulty", "Death-Row"], font=("Roboto", 11))
            dropdown.pack(pady=5, fill="x", padx=10)
            dropdown.is_conditional = True
            self.widgets.extend([label, dropdown])
            self.fields.append((customer_battery_condition_var, "Battery Condition:"))
            dropdown.bind("<<ComboboxSelected>>", lambda e: self.update_workflow_message())
        elif source == "Supplier":
            workflow = "Store and monitor its health."
            workflow_label = tk.Label(self.content, text=workflow, font=("Roboto", 11), bg="#f0f0f0", fg="#333333", wraplength=700)
            workflow_label.pack(pady=5, fill="x", padx=10)
            workflow_label.is_conditional = True
            self.widgets.append(workflow_label)

        if source == "Customer" and customer_battery_condition_var.get():
            self.update_workflow_message()

    def update_workflow_message(self):
        for widget in self.widgets:
            if hasattr(widget, "is_workflow") and widget.is_workflow:
                widget.destroy()
        self.widgets = [w for w in self.widgets if not (hasattr(w, "is_workflow") and w.is_workflow)]

        condition = customer_battery_condition_var.get().strip()
        if condition == "Faulty":
            workflow = "Diagnostic analysis, disassembly, repair, reassembly, testing, and recertification."
        elif condition == "Death-Row":
            workflow = "Take apart carefully, shred into tiny pieces, then into powder for use in making new batteries elsewhere."
        else:
            return

        workflow_label = tk.Label(self.content, text=workflow, font=("Roboto", 11), bg="#f0f0f0", fg="#333333", wraplength=700)
        workflow_label.pack(pady=5, fill="x", padx=10)
        workflow_label.is_workflow = True
        self.widgets.append(workflow_label)

    def validate_and_proceed(self):
        for var, label in self.fields:
            if not var.get().strip():
                messagebox.showerror("Missing Information", f"Please complete: {label}", parent=root)
                return
        if source_var.get() == "Customer" and not customer_battery_condition_var.get().strip():
            messagebox.showerror("Missing Information", "Please specify the battery condition.", parent=root)
            return
        show_frame(frames["PhotoPage"])

# PhotoPage
class PhotoPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#fafafa")
        self.controller = controller
        self.cap = None
        self.preview_running = False
        self.photo_path = None

        # Header
        header_photo = tk.Frame(self, bg="#4CAF50")
        header_photo.pack(fill="x")
        tk.Label(header_photo, text="Step 6: Take Photo", font=("Roboto", 14, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(pady=15)

        # Content
        content_photo = tk.Frame(self, bg="#f0f0f0", bd=1, relief="solid")
        content_photo.pack(pady=10, padx=10, fill="both", expand=True)
        tk.Label(content_photo, text="Capture item photo:", font=("Roboto", 12, "bold"), bg="#f0f0f0", fg="#212121").pack(pady=10)

        # Preview label
        self.preview_label = tk.Label(content_photo, bg="#f0f0f0")
        self.preview_label.pack(pady=10)

        # Buttons
        btn_frame = tk.Frame(content_photo, bg="#f0f0f0")
        btn_frame.pack(pady=10)
        self.capture_btn = ttk.Button(btn_frame, text="Capture", style="Primary.TButton", command=self.capture_photo)
        self.capture_btn.pack(side="left", padx=5)
        self.retake_btn = ttk.Button(btn_frame, text="Retake", style="Secondary.TButton", command=self.retake_photo, state="disabled")
        self.retake_btn.pack(side="left", padx=5)

        # Navigation
        nav_frame_photo = tk.Frame(content_photo, bg="#f0f0f0")
        nav_frame_photo.pack(pady=10)
        back_btn_photo = ttk.Button(nav_frame_photo, text="Back", style="Secondary.TButton", command=lambda: go_back(self))
        back_btn_photo.pack(side="left", padx=5)
        next_btn_photo = ttk.Button(nav_frame_photo, text="Next", style="Primary.TButton", command=lambda: go_next(self, frames["ReactionPage"], photo_taken.get(), "Photo capture"))
        next_btn_photo.pack(side="left", padx=5)

    def start_camera(self):
        self.stop_camera()
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                messagebox.showerror("Camera Error", "Failed to access camera. Please ensure the camera is connected and not in use.", parent=root)
                self.cap = None
                return
        except Exception as e:
            messagebox.showerror("Camera Error", f"Error initializing camera: {str(e)}", parent=root)
            self.cap = None
            return

        self.preview_running = True
        self.update_preview()

    def update_preview(self):
        if not self.preview_running or not self.cap:
            return

        try:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.resize(frame, (320, 240))
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                imgtk = ImageTk.PhotoImage(image=img)
                self.preview_label.imgtk = imgtk
                self.preview_label.configure(image=imgtk)
            else:
                messagebox.showwarning("Camera Warning", "Failed to read frame from camera.", parent=root)
                self.stop_camera()
                return
        except Exception as e:
            messagebox.showerror("Preview Error", f"Error updating preview: {str(e)}", parent=root)
            self.stop_camera()
            return

        self.after(10, self.update_preview)

    def capture_photo(self):
        if not self.cap or not self.cap.isOpened():
            messagebox.showerror("Camera Error", "Camera is not available. Please restart the application.", parent=root)
            return

        try:
            ret, frame = self.cap.read()
            if ret:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                self.photo_path = f"photo_{timestamp}.jpg"
                if not os.access(".", os.W_OK):
                    messagebox.showerror("Storage Error", "No write permission in the current directory.", parent=root)
                    return
                cv2.imwrite(self.photo_path, frame)
                photo_taken.set(True)
                self.capture_btn.configure(state="disabled")
                self.retake_btn.configure(state="normal")
                messagebox.showinfo("Photo Captured", f"Photo saved as {self.photo_path}", parent=root)
            else:
                messagebox.showerror("Capture Error", "Failed to capture photo.", parent=root)
        except Exception as e:
            messagebox.showerror("Capture Error", f"Error saving photo: {str(e)}", parent=root)

    def retake_photo(self):
        if self.photo_path and os.path.exists(self.photo_path):
            try:
                os.remove(self.photo_path)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete photo: {str(e)}", parent=root)
        photo_taken.set(False)
        self.capture_btn.configure(state="normal")
        self.retake_btn.configure(state="disabled")
        self.start_camera()

    def stop_camera(self):
        self.preview_running = False
        if self.cap:
            try:
                self.cap.release()
            except Exception as e:
                print(f"Error releasing camera: {str(e)}")
            self.cap = None
        self.preview_label.configure(image="")

# ScanPage with Manual Entry
class ScanPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#fafafa")
        self.controller = controller

        # Header
        header_scan = tk.Frame(self, bg="#4CAF50")
        header_scan.pack(fill="x")
        tk.Label(header_scan, text="Step 4: Enter Item Barcode", font=("Roboto", 14, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(pady=15)

        # Content
        content_scan = tk.Frame(self, bg="#f0f0f0", bd=1, relief="solid")
        content_scan.pack(pady=10, padx=10, fill="both", expand=True)
        tk.Label(content_scan, text="Enter the barcode:", font=("Roboto", 12, "bold"), bg="#f0f0f0", fg="#212121").pack(pady=10)

        # Barcode entry field
        self.barcode_entry = ttk.Entry(content_scan, textvariable=barcode_var, font=("Roboto", 11))
        self.barcode_entry.pack(pady=5, fill="x", padx=10)
        self.barcode_entry.focus_set()
        self.barcode_entry.bind("<Return>", lambda e: go_next(self, frames["OperationSpecificPage"], barcode_var.get().strip(), "Barcode entry"))

        # Navigation
        nav_frame_scan = tk.Frame(content_scan, bg="#f0f0f0")
        nav_frame_scan.pack(pady=10)
        back_btn_scan = ttk.Button(nav_frame_scan, text="Back", style="Secondary.TButton", command=lambda: go_back(self))
        back_btn_scan.pack(side="left", padx=5)
        next_btn_scan = ttk.Button(nav_frame_scan, text="Next", style="Primary.TButton", command=lambda: go_next(self, frames["OperationSpecificPage"], barcode_var.get().strip(), "Barcode entry"))
        next_btn_scan.pack(side="left", padx=5)

    def stop_camera(self):
        # No camera to stop since we're using manual entry
        pass

# ReactionPage
class ReactionPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#fafafa")
        self.controller = controller

        # Header
        header_reaction = tk.Frame(self, bg="#4CAF50")
        header_reaction.pack(fill="x")
        tk.Label(header_reaction, text="Step 7: How Are You Feeling?", font=("Roboto", 14, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(pady=15)

        # Content
        content_reaction = tk.Frame(self, bg="#f0f0f0", bd=1, relief="solid")
        content_reaction.pack(pady=10, padx=10, fill="both", expand=True)
        tk.Label(content_reaction, text="Share your feelings about the activity:", font=("Roboto", 12, "bold"), bg="#f0f0f0", fg="#212121").pack(pady=10)

        tk.Label(content_reaction, text="I feel:", font=("Roboto", 11), bg="#f0f0f0", fg="#333333").pack(pady=5)
        adjective_dropdown = ttk.Combobox(content_reaction, textvariable=adjective_var, values=["Excited", "Tired", "Confident", "Frustrated", "Happy", "Bored"], font=("Roboto", 11))
        adjective_dropdown.pack(pady=5, fill="x", padx=10)

        tk.Label(content_reaction, text="Because it’s:", font=("Roboto", 11), bg="#f0f0f0", fg="#333333").pack(pady=5)
        reason_dropdown = ttk.Combobox(content_reaction, textvariable=reason_var, values=["challenging", "routine", "rewarding", "stressful", "fun", "tedious"], font=("Roboto", 11))
        reason_dropdown.pack(pady=5, fill="x", padx=10)

        self.madlib_label = tk.Label(content_reaction, text="", font=("Roboto", 11), bg="#f0f0f0", fg="#666666", wraplength=700)
        self.madlib_label.pack(pady=10)

        adjective_dropdown.bind("<<ComboboxSelected>>", lambda e: self.update_madlib())
        reason_dropdown.bind("<<ComboboxSelected>>", lambda e: self.update_madlib())

        nav_frame_reaction = tk.Frame(content_reaction, bg="#f0f0f0")
        nav_frame_reaction.pack(pady=10)
        back_btn_reaction = ttk.Button(nav_frame_reaction, text="Back", style="Secondary.TButton", command=lambda: go_back(self))
        back_btn_reaction.pack(side="left", padx=5)
        next_btn_reaction = ttk.Button(nav_frame_reaction, text="Next", style="Primary.TButton", command=self.validate_and_proceed)
        next_btn_reaction.pack(side="left", padx=5)

    def update_madlib(self):
        adjective = adjective_var.get().strip()
        reason = reason_var.get().strip()
        activity = action_var.get().strip()
        if adjective and reason and activity:
            sentence = f"I feel {adjective} about {activity} because it’s {reason}."
            self.madlib_label.configure(text=sentence)
        else:
            self.madlib_label.configure(text="")

    def validate_and_proceed(self):
        if not adjective_var.get().strip():
            messagebox.showerror("Missing Information", "Please select how you feel", parent=root)
            return
        if not reason_var.get().strip():
            messagebox.showerror("Missing Information", "Please select a reason", parent=root)
            return
        messagebox.showinfo("Reaction Recorded", "Your reaction has been recorded!", parent=root)
        show_frame(frames["ConfirmationPage"])

# ConfirmationPage
class ConfirmationPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#fafafa")
        self.controller = controller

        # Header
        header_confirm = tk.Frame(self, bg="#4CAF50")
        header_confirm.pack(fill="x")
        tk.Label(header_confirm, text="Step 8: Confirm Details", font=("Roboto", 14, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(pady=15)

        # Content
        content_confirm = tk.Frame(self, bg="#f0f0f0", bd=1, relief="solid")
        content_confirm.pack(pady=10, padx=10, fill="both", expand=True)
        tk.Label(content_confirm, text="Review your submission:", font=("Roboto", 12, "bold"), bg="#f0f0f0", fg="#212121").pack(pady=10)

        tk.Label(content_confirm, text="Technician ID:", font=("Roboto", 11, "bold"), bg="#f0f0f0", fg="#212121", anchor="w").pack(fill="x", padx=10)
        tk.Label(content_confirm, text=user_id_var.get() or "N/A", font=("Roboto", 11), bg="#f0f0f0", fg="#333333", anchor="w").pack(fill="x", padx=10)

        tk.Label(content_confirm, text="Location:", font=("Roboto", 11, "bold"), bg="#f0f0f0", fg="#212121", anchor="w").pack(fill="x", padx=10)
        tk.Label(content_confirm, text=location_var.get() or "N/A", font=("Roboto", 11), bg="#f0f0f0", fg="#333333", anchor="w").pack(fill="x", padx=10)

        tk.Label(content_confirm, text="Action:", font=("Roboto", 11, "bold"), bg="#f0f0f0", fg="#212121", anchor="w").pack(fill="x", padx=10)
        tk.Label(content_confirm, text=action_var.get() or "N/A", font=("Roboto", 11), bg="#f0f0f0", fg="#333333", anchor="w").pack(fill="x", padx=10)

        tk.Label(content_confirm, text="Barcode:", font=("Roboto", 11, "bold"), bg="#f0f0f0", fg="#212121", anchor="w").pack(fill="x", padx=10)
        tk.Label(content_confirm, text=barcode_var.get() or "N/A", font=("Roboto", 11), bg="#f0f0f0", fg="#333333", anchor="w").pack(fill="x", padx=10)

        operation = action_var.get().strip()
        if operation in OPERATION_TEMPLATES and OPERATION_TEMPLATES[operation]["fields"]:
            for field in OPERATION_TEMPLATES[operation]["fields"]:
                if field.get("lookup"):
                    continue
                tk.Label(content_confirm, text=field["label"], font=("Roboto", 11, "bold"), bg="#f0f0f0", fg="#212121", anchor="w").pack(fill="x", padx=10)
                if field["variable"] == "new_location_var":
                    value = new_location_var.get()
                elif field["variable"] == "battery_condition_var":
                    value = battery_condition_var.get()
                elif field["variable"] == "destination_var":
                    value = destination_var.get()
                elif field["variable"] == "source_var":
                    value = source_var.get()
                else:
                    value = "N/A"
                tk.Label(content_confirm, text=value or "N/A", font=("Roboto", 11), bg="#f0f0f0", fg="#333333", anchor="w").pack(fill="x", padx=10)

        if operation == "Receive" and source_var.get() == "Customer":
            tk.Label(content_confirm, text="Battery Condition:", font=("Roboto", 11, "bold"), bg="#f0f0f0", fg="#212121", anchor="w").pack(fill="x", padx=10)
            tk.Label(content_confirm, text=customer_battery_condition_var.get() or "N/A", font=("Roboto", 11), bg="#f0f0f0", fg="#333333", anchor="w").pack(fill="x", padx=10)

        tk.Label(content_confirm, text="Photo Path:", font=("Roboto", 11, "bold"), bg="#f0f0f0", fg="#212121", anchor="w").pack(fill="x", padx=10)
        photo_path = frames["PhotoPage"].photo_path if frames["PhotoPage"].photo_path else "N/A"
        tk.Label(content_confirm, text=photo_path, font=("Roboto", 11), bg="#f0f0f0", fg="#333333", anchor="w").pack(fill="x", padx=10)

        tk.Label(content_confirm, text="Reaction:", font=("Roboto", 11, "bold"), bg="#f0f0f0", fg="#212121", anchor="w").pack(fill="x", padx=10)
        reaction = f"I feel {adjective_var.get()} about {action_var.get()} because it’s {reason_var.get()}." if adjective_var.get() and reason_var.get() else "N/A"
        tk.Label(content_confirm, text=reaction, font=("Roboto", 11), bg="#f0f0f0", fg="#666666", anchor="w", wraplength=700).pack(fill="x", padx=10)

        nav_frame_confirm = tk.Frame(content_confirm, bg="#f0f0f0")
        nav_frame_confirm.pack(pady=10)
        back_btn_confirm = ttk.Button(nav_frame_confirm, text="Back", style="Secondary.TButton", command=lambda: go_back(self))
        back_btn_confirm.pack(side="left", padx=5)
        next_btn_confirm = ttk.Button(nav_frame_confirm, text="Next", style="Primary.TButton", command=lambda: show_frame(frames["DonePage"]))
        next_btn_confirm.pack(side="left", padx=5)

# DonePage
class DonePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#fafafa")
        self.controller = controller
        self.operation_id = None

        # Header
        header_done = tk.Frame(self, bg="#4CAF50")
        header_done.pack(fill="x")
        tk.Label(header_done, text="Step 9: Done", font=("Roboto", 14, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(pady=15)

        # Content
        content_done = tk.Frame(self, bg="#f0f0f0", bd=1, relief="solid")
        content_done.pack(pady=10, padx=10, fill="both", expand=True)

        tk.Label(content_done, text="SPIERS System", font=("Roboto", 16, "bold"), bg="#f0f0f0", fg="#212121").pack(pady=10)
        tk.Label(content_done, text="Thank you!\nOperation logged.", font=("Roboto", 11), bg="#f0f0f0", fg="#333333").pack(pady=10)

        # Summary section
        tk.Label(content_done, text="Operation Summary:", font=("Roboto", 12, "bold"), bg="#f0f0f0", fg="#212121").pack(pady=5)
        self.summary_text = tk.Text(content_done, height=8, width=50, font=("Roboto", 11), bg="#f0f0f0", fg="#333333", wrap="word")
        self.summary_text.pack(pady=5, padx=10)
        self.summary_text.config(state="disabled")

        # Buttons
        tk.Label(content_done, text="Next?", font=("Roboto", 12, "bold"), bg="#f0f0f0", fg="#212121").pack(pady=10)
        btn_frame = tk.Frame(content_done, bg="#f0f0f0")
        btn_frame.pack(pady=10)
        save_btn = ttk.Button(btn_frame, text="Save Summary", style="Primary.TButton", command=self.save_summary)
        save_btn.pack(side="left", padx=5)
        new_op_btn = ttk.Button(btn_frame, text="New Op", style="Primary.TButton", command=self.start_new_operation)
        new_op_btn.pack(side="left", padx=5)
        exit_btn = ttk.Button(btn_frame, text="Exit", style="Exit.TButton", command=root.destroy)
        exit_btn.pack(side="left", padx=5)

    def tkraise(self, *args, **kwargs):
        # Log the operation when this page is shown
        self.operation_id = log_operation()
        if self.operation_id:
            # Generate and display the summary
            summary = generate_operation_summary(self.operation_id)
            self.summary_text.config(state="normal")
            self.summary_text.delete("1.0", tk.END)
            self.summary_text.insert(tk.END, summary)
            self.summary_text.config(state="disabled")
        super().tkraise(*args, **kwargs)

    def save_summary(self):
        if not self.operation_id:
            messagebox.showerror("Error", "No operation to summarize.", parent=root)
            return
        summary = generate_operation_summary(self.operation_id)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"operation_summary_{self.operation_id}_{timestamp}.txt"
        try:
            with open(filename, "w") as f:
                f.write(summary)
            messagebox.showinfo("Success", f"Summary saved as {filename}", parent=root)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save summary: {str(e)}", parent=root)

    def start_new_operation(self):
        reset_variables()
        self.operation_id = None
        self.summary_text.config(state="normal")
        self.summary_text.delete("1.0", tk.END)
        self.summary_text.config(state="disabled")
        show_frame(frames["StartPage"])

# Main container setup
container = tk.Frame(root, bg="#fafafa")
container.pack(fill="both", expand=True)
container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)

# Create all frames
frames = {}
for F in ("StartPage", "UserPage", "LocationPage", "ActivityPage", "ScanPage", "OperationSpecificPage", "PhotoPage", "ReactionPage", "ConfirmationPage", "DonePage"):
    if F == "OperationSpecificPage":
        frame = OperationSpecificPage(container, None)
    elif F == "PhotoPage":
        frame = PhotoPage(container, None)
    elif F == "ScanPage":
        frame = ScanPage(container, None)
    elif F == "ReactionPage":
        frame = ReactionPage(container, None)
    elif F == "ConfirmationPage":
        frame = ConfirmationPage(container, None)
    elif F == "DonePage":
        frame = DonePage(container, None)
    else:
        frame = tk.Frame(container, bg="#fafafa")
    frames[F] = frame
    frame.grid(row=0, column=0, sticky="nsew")

# Start Page
start_frame = frames["StartPage"]
header_start = tk.Frame(start_frame, bg="#4CAF50")
header_start.pack(fill="x")
tk.Label(header_start, text="SPIERS Smart System", font=("Roboto", 16, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(pady=15)

content_start = tk.Frame(start_frame, bg="#f0f0f0", bd=1, relief="solid")
content_start.pack(pady=10, padx=10, fill="both", expand=True)
start_btn = ttk.Button(content_start, text="Start Session", style="Primary.TButton", command=lambda: show_frame(frames["UserPage"]))
start_btn.pack(pady=10)

try:
    logo_img = Image.open("logo.jpg")
    logo_img = logo_img.resize((300, int(300 * logo_img.height / logo_img.width)), Image.LANCZOS)
    logo_image = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(content_start, image=logo_image, bg="#f0f0f0")
    logo_label.image = logo_image
    logo_label.pack(pady=10)
except Exception as e:
    print(f"Error loading logo image: {e}")
    tk.Label(content_start, text="[Logo Failed to Load]", font=("Roboto", 11), bg="#f0f0f0", fg="red").pack(pady=10)

# User Page with MariaDB Authentication
class UserPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#fafafa")
        self.controller = controller

        # Header
        header_user = tk.Frame(self, bg="#4CAF50")
        header_user.pack(fill="x")
        tk.Label(header_user, text="Step 1: Technician Login", font=("Roboto", 14, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(pady=15)

        # Content
        content_user = tk.Frame(self, bg="#f0f0f0", bd=1, relief="solid")
        content_user.pack(pady=10, padx=10, fill="both", expand=True)
        tk.Label(content_user, text="Please log in:", font=("Roboto", 12, "bold"), bg="#f0f0f0", fg="#212121").pack(pady=10)

        tk.Label(content_user, text="User ID:", font=("Roboto", 11), bg="#f0f0f0", fg="#333333").pack(pady=5)
        user_id_entry = ttk.Entry(content_user, textvariable=user_id_var, font=("Roboto", 11))
        user_id_entry.pack(pady=5, fill="x", padx=10)
        user_id_entry.focus_set()

        tk.Label(content_user, text="Password:", font=("Roboto", 11), bg="#f0f0f0", fg="#333333").pack(pady=5)
        password_entry = ttk.Entry(content_user, textvariable=password_var, font=("Roboto", 11), show="*")
        password_entry.pack(pady=5, fill="x", padx=10)

        nav_frame_user = tk.Frame(content_user, bg="#f0f0f0")
        nav_frame_user.pack(pady=10)
        back_btn_user = ttk.Button(nav_frame_user, text="Back", style="Secondary.TButton", command=lambda: go_back(self))
        back_btn_user.pack(side="left", padx=5)
        next_btn_user = ttk.Button(nav_frame_user, text="Next", style="Primary.TButton", command=self.validate_and_proceed)
        next_btn_user.pack(side="left", padx=5)

    def validate_and_proceed(self):
        user_id = user_id_var.get().strip()
        password = password_var.get().strip()
        if not user_id or not password:
            messagebox.showerror("Missing Information", "Please enter both User ID and Password", parent=root)
            return

        # Hash the entered password using SHA-256
        entered_password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

        # Check credentials against the MariaDB database
        try:
            conn = mysql.connector.connect(
                host="127.0.0.1",
                user="spiers_user",
                password="spiers_pass",
                database="spiers_system",
                auth_plugin="mysql_native_password"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT password_hash FROM users WHERE user_id = %s", (user_id,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()

            if result:
                stored_password_hash = result[0]
                if entered_password_hash == stored_password_hash:
                    show_frame(frames["LocationPage"])
                else:
                    messagebox.showerror("Authentication Failed", "Invalid User ID or Password", parent=root)
                    password_var.set("")
            else:
                messagebox.showerror("Authentication Failed", "Invalid User ID or Password", parent=root)
                password_var.set("")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error accessing database: {str(err)}", parent=root)
            password_var.set("")

frames["UserPage"] = UserPage(container, None)
frames["UserPage"].grid(row=0, column=0, sticky="nsew")

# Location Page
location_frame = frames["LocationPage"]
header_location = tk.Frame(location_frame, bg="#4CAF50")
header_location.pack(fill="x")
tk.Label(header_location, text="Step 2: Location", font=("Roboto", 14, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(pady=15)

content_location = tk.Frame(location_frame, bg="#f0f0f0", bd=1, relief="solid")
content_location.pack(pady=10, padx=10, fill="both", expand=True)
tk.Label(content_location, text="Where are you?", font=("Roboto", 12, "bold"), bg="#f0f0f0", fg="#212121").pack(pady=10)
location_dropdown = ttk.Combobox(content_location, textvariable=location_var, values=["New Battery Section", "Old Battery Section"], font=("Roboto", 11))
location_dropdown.pack(pady=5, fill="x", padx=10)

nav_frame_location = tk.Frame(content_location, bg="#f0f0f0")
nav_frame_location.pack(pady=10)
back_btn_location = ttk.Button(nav_frame_location, text="Back", style="Secondary.TButton", command=lambda: go_back(location_frame))
back_btn_location.pack(side="left", padx=5)
next_btn_location = ttk.Button(nav_frame_location, text="Next", style="Primary.TButton", command=lambda: go_next(location_frame, frames["ActivityPage"], location_var.get(), "Location selection"))
next_btn_location.pack(side="left", padx=5)

# Activity Page
activity_frame = frames["ActivityPage"]
header_activity = tk.Frame(activity_frame, bg="#4CAF50")
header_activity.pack(fill="x")
tk.Label(header_activity, text="Step 3: Action", font=("Roboto", 14, "bold"), bg="#4CAF50", fg="#FFFFFF").pack(pady=15)

content_activity = tk.Frame(activity_frame, bg="#f0f0f0", bd=1, relief="solid")
content_activity.pack(pady=10, padx=10, fill="both", expand=True)
tk.Label(content_activity, text="What are you doing?", font=("Roboto", 12, "bold"), bg="#f0f0f0", fg="#212121").pack(pady=10)
activity_dropdown = ttk.Combobox(content_activity, textvariable=action_var, values=["Find", "Receive", "Ship", "Move"], font=("Roboto", 11))
activity_dropdown.pack(pady=5, fill="x", padx=10)

nav_frame_activity = tk.Frame(content_activity, bg="#f0f0f0")
nav_frame_activity.pack(pady=10)
back_btn_activity = ttk.Button(nav_frame_activity, text="Back", style="Secondary.TButton", command=lambda: go_back(activity_frame))
back_btn_activity.pack(side="left", padx=5)
next_btn_activity = ttk.Button(nav_frame_activity, text="Next", style="Primary.TButton", command=lambda: go_next(activity_frame, frames["ScanPage"], action_var.get(), "Action selection"))
next_btn_activity.pack(side="left", padx=5)

# Start with StartPage
show_frame(frames["StartPage"])

# Run the main loop
root.mainloop()
