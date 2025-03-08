import json
import datetime
import pytest
import pprint

from query_handler import (
    extract_flight_parameters,
    search_flights,
    process_response
)
from mock_database import flight_data

# Dummy Gemini responses for testing extraction, including proper JSON, markdown wrapped JSON, 
# invalid JSON, and an exception case.
def dummy_generate_gemini_response(prompt: str) -> str:
    if "Extract flight information" in prompt:
        return json.dumps({
            "flight_number": None,
            "origin": "New York",
            "destination": "London",
            "date": "2025-03-05",
            "time": "10:00",
            "before_date": None,
            "after_date": None,
            "before_time": None,
            "after_time": None
        })
    else:
        return "Final dummy response using flight data."

def dummy_generate_invalid_json(prompt: str) -> str:
    return "Not a valid JSON response"

def dummy_generate_markdown_response(prompt: str) -> str:
    if "Extract flight information" in prompt:
        response_dict = {
            "flight_number": None,
            "origin": "Paris",
            "destination": "Dubai",
            "date": "2025-03-03",
            "time": "14:55",
            "before_date": None,
            "after_date": None,
            "before_time": None,
            "after_time": None
        }
        return "```json\n" + json.dumps(response_dict) + "\n```"
    else:
        return "Final dummy response using flight data."

def dummy_generate_exception(prompt: str) -> str:
    raise Exception("Gemini API error")

# Fixtures to facilitate monkeypatching Gemini API responses.

@pytest.fixture
def set_dummy_gemini(monkeypatch):
    """
    A fixture to set the dummy Gemini generator.
    Usage: pass the specific dummy response function as an argument.
    """
    def _set_dummy(dummy_func):
        monkeypatch.setattr("query_handler.generate_gemini_response", dummy_func)
    return _set_dummy

# =====================
# Extraction Tests
# =====================

def test_extract_flight_parameters_success(set_dummy_gemini):
    set_dummy_gemini(dummy_generate_gemini_response)
    query = "Show flights from New York to London at 10 am"
    params = extract_flight_parameters(query)
    
    # Check expected values.
    assert isinstance(params, dict)
    assert params.get("origin") == "New York"
    assert params.get("destination") == "London"
    assert params.get("date") == "2025-03-05"
    assert params.get("time") == "10:00"
    # Other keys should be present and set to None.
    for key in ["flight_number", "before_date", "after_date", "before_time", "after_time"]:
        assert params.get(key) is None

def test_extract_flight_parameters_failure(set_dummy_gemini):
    set_dummy_gemini(dummy_generate_invalid_json)
    query = "Invalid query"
    with pytest.raises(ValueError, match="Failed to parse Gemini response"):
        extract_flight_parameters(query)

def test_extract_flight_parameters_with_markdown(set_dummy_gemini):
    set_dummy_gemini(dummy_generate_markdown_response)
    query = "Show flights from Paris to Dubai"
    params = extract_flight_parameters(query)
    
    assert params.get("origin") == "Paris"
    assert params.get("destination") == "Dubai"
    assert params.get("date") == "2025-03-03"
    assert params.get("time") == "14:55"

# =====================
# Search Tests
# =====================

@pytest.mark.parametrize("parameters, expected_flight_numbers, description", [
    (
        {
            "flight_number": None,
            "origin": "New York",
            "destination": "London",
            "date": "2025-03-05",
            "time": "10:00",
            "before_date": None,
            "after_date": None,
            "before_time": None,
            "after_time": None,
        },
        ["AA101"],
        "Expect flight AA101 when searching by origin, destination, date and time"
    ),
    (
        {
            "flight_number": None,
            "origin": "NonExistentCity",
            "destination": "London",
            "date": "2025-03-05",
            "time": "10:00",
            "before_date": None,
            "after_date": None,
            "before_time": None,
            "after_time": None,
        },
        [],
        "Expect no flights if origin does not match"
    ),
    (
        {
            "flight_number": "DL303",
            "origin": None,
            "destination": None,
            "date": None,
            "time": None,
            "before_date": None,
            "after_date": None,
            "before_time": None,
            "after_time": None,
        },
        ["DL303"],
        "Expect exact flight match when querying by flight number"
    ),
    (
        {
            "flight_number": None,
            "origin": None,
            "destination": None,
            "date": None,
            "time": None,
            "before_date": None,
            "after_date": None,
            "before_time": None,
            "after_time": None,
        },
        [flight["flight_number"] for flight in flight_data],
        "Expect all flights when all parameters are None"
    ),
])
def test_search_flights(parameters, expected_flight_numbers, description):
    flights = search_flights(parameters)
    flight_numbers = [flight["flight_number"] for flight in flights]
    for num in expected_flight_numbers:
        assert num in flight_numbers, description

def test_search_flights_date_and_time_intervals():
    parameters = {
        "flight_number": None,
        "origin": "New York",
        "destination": "London",
        "date": None,
        "time": None,
        "before_date": "2025-03-06",  # On or before March 6, 2025.
        "after_date": "2025-03-04",   # On or after March 4, 2025.
        "before_time": "11:00",       # On or before 11:00.
        "after_time": "09:00",        # On or after 09:00.
    }
    flights = search_flights(parameters)
    # Expect flight "AA101" to match.
    assert len(flights) == 1
    assert flights[0]["flight_number"] == "AA101"

def test_search_flights_case_insensitive():
    parameters = {
        "flight_number": None,
        "origin": "new york",  # lower-case input
        "destination": "london",  # lower-case input
        "date": "2025-03-05",
        "time": "10:00",
        "before_date": None,
        "after_date": None,
        "before_time": None,
        "after_time": None,
    }
    flights = search_flights(parameters)
    assert any(flight["flight_number"] == "AA101" for flight in flights)

# =====================
# Process Response Tests
# =====================

def test_process_response_success(set_dummy_gemini):
    # Both extraction and final response use the dummy.
    set_dummy_gemini(dummy_generate_gemini_response)
    query = "What are the flights from New York to London?"
    response = process_response(query)
    assert response == "Final dummy response using flight data."

def test_process_response_failure(set_dummy_gemini):
    # Simulate an error in the Gemini API call during the final response.
    set_dummy_gemini(dummy_generate_exception)
    query = "What are the flights from New York to London?"
    with pytest.raises(Exception, match="Gemini API error"):
        process_response(query)