import logging
from mock_database import flight_data
from gemini_api import generate_gemini_response
import datetime
import json
import re
from utils import convert_date, convert_time
from typing import Optional
import pprint # Temporarily using so parameters and flights look better when printed

def extract_flight_parameters(user_query: str) -> dict[str, Optional[str]]:
    """
    Extract flight information from a users query using Gemini 

    Args:
        user_query (str): the users query about flight information

    Returns:
        dict[str, Optional[str]]: a dictionary containing flight parameters
    """

    # Get todays date so gemini knows what todays date and can use that information to answer time relative questions
    today = datetime.datetime.now().strftime("%Y-%m-%d") 

    prompt = f"""
    Today's date is {today}. If the user's query refers to a time (e.g., '10 am') or a location but does not mention a specific date, assume they are referring to today.
    If the user's query is in another language, put the parameters in english

    Extract flight information from the following query:
    "{user_query}"
    
    Return a JSON object with these keys:
    - flight_number: str or null
    - origin: str or null
    - destination: str or null
    - date: str in YYYY-MM-DD format or null
    - time: str in HH:MM format or null
    - before_date: str in YYYY-MM-DD format or null
    - after_date: str in YYYY-MM-DD format or null
    - before_time: str in HH:MM format or null
    - after_time: str in HH:MM format or null
    """

    response = generate_gemini_response(prompt)

    try: 
        # Clean Gemini's markdown formatting if any
        cleaned_response = re.sub(r'```json\n|\n```', '', response)
        print(cleaned_response)
        # Convert extracted text into a Python dictionary
        parsed_json = json.loads(cleaned_response)

        return parsed_json
    except Exception as e:
        raise ValueError(f"Failed to parse Gemini response: {e}")

def search_flights(parameters: dict[str, Optional[str]]) -> list[dict[str, Optional[str]]]:
    """
    Given parameters it searches a mock database of flights to find flights matching
    those parameters

    Args:
        parameters (dict[str, Optional[str]]): A dictionary containing parameters for searching flights

    Returns:
        list[dict[str, Optional[str]]]: A list of flights matching the given criteria
    """

    # Extract parameters from the python dictionary
    flight_number = parameters.get("flight_number")
    origin = parameters.get("origin")
    destination = parameters.get("destination")
    date = convert_date(parameters.get("date"))
    time = convert_time(parameters.get("time"))
    before_date = convert_date(parameters.get("before_date"))
    after_date = convert_date(parameters.get("after_date"))
    before_time = convert_time(parameters.get("before_time"))
    after_time = convert_time(parameters.get("after_time"))

    # Find flights matching the given parameters and intervals
    return [
        flight for flight in flight_data
        if (flight_number is None or flight.get('flight_number') == flight_number)
        and (origin is None or flight.get('origin').lower() == origin.lower())
        and (destination is None or flight.get('destination').lower() == destination.lower())
        and (date is None or flight.get("date") == date)
        and (time is None or flight.get('time') == time)
        and (before_date is None or flight.get("date") <= before_date)
        and (after_date is None or flight.get("date") >= after_date)
        and (before_time is None or flight.get('time') <= before_time)
        and (after_time is None or flight.get('time') >= after_time)
    ]

def process_response(query: str) -> str:
    """
    Processes a user's query by extracting the parameters, searching for
    relevant flight information and generating a response from Gemini 
    using that information

    Args:
        query (str): The user's query about flight information

    Returns:
        str: Gemini's answer to the users query using relevant flight information
    """

    parameters = extract_flight_parameters(query)
    logging.info(f"\n Parameters:\n {pprint.pformat(parameters)}")

    flights = search_flights(parameters)
    logging.info(f"\nFlights Found:\n {pprint.pformat(flights)}")

    prompt = f"""
    Here is the User's Query: {query}

    Here is some Relevant Flight Information we found based on it: {flights}

    Now you should answer their question using the given flight information.

    Remember you are speaking directly to the user.
    """

    response = generate_gemini_response(prompt)

    return response