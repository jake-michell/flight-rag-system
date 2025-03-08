import datetime
from typing import Optional
import logging

def convert_time(time_string: Optional[str]) -> Optional[datetime.time]:
    """
    Converts a string representing a time in the iso format HH:MM to a time object

    Args: 
        time_string (Optional[str]): a string in iso format HH:MM or None

    Return: 
        Optional[datetime.time]: time object if the conversion was successful otherwise None
    """

    # early exit if input is None
    if time_string is None:
        return None

    try:
        return datetime.time.fromisoformat(time_string)
    except ValueError as e:
        logging.error(f"Time conversion failed for input {time_string}: {e}")
        return None

def convert_date(date_string: Optional[str]) -> Optional[datetime.date]:
    """
    Converts a string representing a date in the iso format YYYY-MM-DD to a date object

    Args: 
        date_string (Optional[str]): a string in iso format YYYY-MM-DD or None

    Returns: 
        Optional[datetime.date]: a date object if the conversion was successful otherwise None
    """

    # early exit if input is None
    if date_string is None:
        return None

    try:
        return datetime.date.fromisoformat(date_string)
    except ValueError as e:
        logging.error(f"Date conversion failed for input {date_string}: {e}")
        return None
