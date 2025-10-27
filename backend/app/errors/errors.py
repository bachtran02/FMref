class FMrefError(Exception):
    """Base class for exceptions in this module."""
    pass

class InvalidFileError(FMrefError):
    """Raised when an uploaded file is invalid."""
    pass

class MissingColumnsError(FMrefError):
    """Raised when required columns are missing from parsed data."""
    def __init__(self, missing_columns):
        self.missing_columns = missing_columns
        super().__init__(f"Missing required columns: {missing_columns}")

class InvalidColumnValueError(FMrefError):
    """Raised when a column has an invalid value."""
    def __init__(self, column_name, message):
        self.column_name = column_name
        super().__init__(f"Invalid value in column '{column_name}': {message}")