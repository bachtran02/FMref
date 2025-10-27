from ..errors.errors import MissingColumnsError

def verify_columns(df, required_columns):
    """
    Verify that the DataFrame contains all required columns.
    
    Raises:
        MissingColumnsError: If any required columns are missing
    """
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise MissingColumnsError(missing_columns)
