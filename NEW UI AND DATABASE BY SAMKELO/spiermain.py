import tkinter as tk
from database_manager import DatabaseManager
from app import SpiersApp
from pages.start_page import StartPage
from pages.user_page import UserPage
from pages.location_page import LocationPage
from pages.activity_page import ActivityPage
from pages.scan_page import ScanPage
from pages.operation_specific_page import OperationSpecificPage
from pages.photo_page import PhotoPage
from pages.reaction_page import ReactionPage
from pages.confirmation_page import ConfirmationPage
from pages.done_page import DonePage

if __name__ == "__main__":
    # Define page classes dictionary
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

    # Initialize database manager
    db_manager = DatabaseManager()

    # Initialize Tkinter root and application
    root = tk.Tk()
    app = SpiersApp(root, page_classes, db_manager)
    root.mainloop()
