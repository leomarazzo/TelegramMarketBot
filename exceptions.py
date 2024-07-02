class NotFoundException(Exception):
    """Raised when the product is not found in the list"""

class BadCommandException(Exception):
    """Raised when the command is incorrect or incomplete"""