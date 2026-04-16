"""
Custom exceptions for the Sprout application.
These help provide clear, user-friendly error messages to the frontend.
"""

class SproutBaseException(Exception):
    """Base exception for all custom Sprout errors."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class InvalidSB3Error(SproutBaseException):
    """Raised when the uploaded file is not a valid ZIP/SB3 archive."""
    pass

class ProjectJSONNotFoundError(SproutBaseException):
    """Raised when an SB3 archive does not contain a project.json file."""
    pass

class ParsingError(SproutBaseException):
    """Raised when the project.json cannot be parsed or fails schema validation."""
    pass