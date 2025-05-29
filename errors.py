class SalaryParsingError(Exception):
    """Raised when there is an error parsing salary or transfer value."""
    pass

class TransferValueParsingError(Exception):
    """Raised when there is an error parsing transfer value."""
    pass

class DistanceParsingError(Exception):
    """Raised when there is an error parsing distance."""
    pass