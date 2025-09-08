class MissingColumnsError(Exception):
    """Raised when the dataframe is missing required columns."""
    pass

class HeightWeightParsingError(Exception):
    """Raised when there is an error parsing height or weight."""
    pass

class SalaryParsingError(Exception):
    """Raised when there is an error parsing salary or transfer value."""
    pass

class TransferValueParsingError(Exception):
    """Raised when there is an error parsing transfer value."""
    pass

class DistanceParsingError(Exception):
    """Raised when there is an error parsing distance."""
    pass
