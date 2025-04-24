import tkinter as tk
from database_manager import DatabaseManager
from app import SpiersApp
from pages import StartPage, UserPage, LocationPage, ActivityPage, ScanPage, OperationSpecificPage, PhotoPage, ReactionPage, ConfirmationPage, DonePage

# Entry point of the application
if __name__ == "__main__":
    # Define a dictionary mapping page names to their respective classes
    page_classes = {
        "StartPage": StartPage,
        "UserPage": UserPage,
        "LocationPage": LocationPage,
        "ActivityPage": ActivityPage,
        "ScanPage": ScanPage,
        "OperationSpecificPage": OperationSpecificPage,
        "PhotoPage": PhotoPage,
        "ReactionPage": ReactionPage,
        "ConfirmationPage": ConfirmationPage,
        "DonePage": DonePage
    }

    # Initialize the database manager for handling database operations
    db_manager = DatabaseManager()

    # Create the main Tkinter window
    root = tk.Tk()
    # Initialize the SpiersApp with the root window, page classes, and database manager
    app = SpiersApp(root, page_classes, db_manager)
    # Start the Tkinter event loop to run the application
    root.mainloop()
