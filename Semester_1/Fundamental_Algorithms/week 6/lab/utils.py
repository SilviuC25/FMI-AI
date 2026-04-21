from datetime import datetime

def is_valid_date(date_str: str) -> bool:
    """
    Checks if the given string is a valid date in DD/MM/YYYY format.
    Returns True if valid, False otherwise.
    """
    try:
        datetime.strptime(date_str, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def is_positive_number(value: float) -> bool:
    """
    Checks if a number is positive.
    """
    return value > 0

def is_non_empty_string(value: str) -> bool:
    """
    Checks if a string is not empty and does not contain only spaces.
    """
    return bool(value.strip())

def convert_string_to_date(date_str: str) -> datetime:
    """
    Parses a date string in DD/MM/YYYY format into a datetime object.
    """
    return datetime.strptime(date_str, "%d/%m/%Y")

