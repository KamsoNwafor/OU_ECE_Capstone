import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

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
