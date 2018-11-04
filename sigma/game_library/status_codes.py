"""Error code enums for game."""
from .custom_enums_classes import CustomIntEnum

class GameStatusCodes(CustomIntEnum):
    """ Api status codes."""

    OK = 0
    ERROR = 1
    DUPLICATE_USERNAME = 2
    AUTH_FAILED = 3
