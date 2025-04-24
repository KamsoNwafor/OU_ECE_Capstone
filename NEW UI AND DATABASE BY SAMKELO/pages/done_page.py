import tkinter as tk
from tkinter import ttk, messagebox
import time

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
