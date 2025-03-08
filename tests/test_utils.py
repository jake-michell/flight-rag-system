import datetime
import logging
import pytest
from utils import convert_date, convert_time

# Tests for convert_time

@pytest.mark.parametrize("time_str, expected_hour, expected_minute, expected_second", [
    ("00:00", 0, 0, 0),
    ("23:59", 23, 59, 0),
    ("12:34", 12, 34, 0),
    ("07:45", 7, 45, 0),
])
def test_convert_time_valid_without_seconds(time_str, expected_hour, expected_minute, expected_second):
    result = convert_time(time_str)
    assert isinstance(result, datetime.time)
    assert result.hour == expected_hour
    assert result.minute == expected_minute
    assert result.second == expected_second

@pytest.mark.parametrize("time_str, expected_hour, expected_minute, expected_second", [
    ("23:59:59", 23, 59, 59),
])
def test_convert_time_valid_with_seconds(time_str, expected_hour, expected_minute, expected_second):
    result = convert_time(time_str)
    assert isinstance(result, datetime.time)
    assert result.hour == expected_hour
    assert result.minute == expected_minute
    assert result.second == expected_second

def test_convert_time_none():
    # Input is None, should return None.
    assert convert_time(None) is None

@pytest.mark.parametrize("time_str", [
    "",             # empty string
    "not a time",   # non-numeric input
    "24:00",        # invalid hour (max is 23)
    "12:60",        # invalid minute
    "12-34",        # wrong separator
    "99:99"         # completely out of range
])
def test_convert_time_invalid(time_str, caplog):
    with caplog.at_level(logging.ERROR):
        result = convert_time(time_str)
        assert result is None
        # Check that an error message was logged.
        assert any("Time conversion failed" in record.message for record in caplog.records)
    caplog.clear()

# Tests for convert_date

@pytest.mark.parametrize("date_str, expected_year, expected_month, expected_day", [
    ("2020-01-01", 2020, 1, 1),
    ("1999-12-31", 1999, 12, 31),
    ("2000-02-29", 2000, 2, 29),  # leap year date
])
def test_convert_date_valid(date_str, expected_year, expected_month, expected_day):
    result = convert_date(date_str)
    assert isinstance(result, datetime.date)
    assert result.year == expected_year
    assert result.month == expected_month
    assert result.day == expected_day

def test_convert_date_none():
    # Input is None, should return None.
    assert convert_date(None) is None

@pytest.mark.parametrize("date_str", [
    "",             # empty string
    "not a date",   # non-date string
    "2020-13-01",   # invalid month
    "2020-00-10",   # invalid month (zero)
    "2020-02-30",   # invalid day
    "01-01-2020",   # wrong format (should be YYYY-MM-DD)
    "2020/01/01"    # wrong separator
])
def test_convert_date_invalid(date_str, caplog):
    with caplog.at_level(logging.ERROR):
        result = convert_date(date_str)
        assert result is None
        # Check that an error message was logged.
        assert any("Date conversion failed" in record.message for record in caplog.records)
    caplog.clear()
