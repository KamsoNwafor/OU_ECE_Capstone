# Import all page classes to make them available when importing the package
from .start_page import StartPage
from .user_page import UserPage
from .location_page import LocationPage
from .activity_page import ActivityPage
from .scan_page import ScanPage
from .operation_specific_page import OperationSpecificPage
from .photo_page import PhotoPage
from .reaction_page import ReactionPage
from .confirmation_page import ConfirmationPage
from .done_page import DonePage

# Define __all__ to specify which names are exported when 'from pages import *' is used
__all__ = [
    "StartPage",
    "UserPage",
    "LocationPage",
    "ActivityPage",
    "ScanPage",
    "OperationSpecificPage",
    "PhotoPage",
    "ReactionPage",
    "ConfirmationPage",
    "DonePage"
]
