import os
import pytest
import requests

# Set a dummy API key so that gemini_api.py doesn't raise an error upon import
os.environ["API_KEY"] = "dummy_key"

from gemini_api import generate_gemini_response

# A helper class to simulate responses from requests.post
class FakeResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code != 200:
            raise requests.HTTPError("HTTP error simulated")

    def json(self):
        return self.json_data

# Fake post method for a successful API call
def fake_post_success(url, headers, json):
    return FakeResponse({
        "candidates": [
            {
                "content": {
                    "parts": [
                        {"text": "Simulated response text"}
                    ]
                }
            }
        ]
    }, 200)

# Fake post method to simulate a RequestException
def fake_post_request_exception(url, headers, json):
    raise requests.RequestException("Simulated request exception")

# Fake post method to simulate a response with missing keys (LookupError)
def fake_post_lookup_error(url, headers, json):
    # Missing the expected keys (e.g. 'candidates')
    return FakeResponse({}, 200)

def test_generate_gemini_response_success(monkeypatch):
    # Use the fake successful post method
    monkeypatch.setattr(requests, "post", fake_post_success)
    prompt = "Test prompt"
    response = generate_gemini_response(prompt)
    assert response == "Simulated response text"

def test_generate_gemini_response_request_exception(monkeypatch):
    # Use the fake post that raises a RequestException
    monkeypatch.setattr(requests, "post", fake_post_request_exception)
    with pytest.raises(requests.RequestException):
        generate_gemini_response("Test prompt")

def test_generate_gemini_response_lookup_error(monkeypatch):
    # Use the fake post that returns a malformed JSON
    monkeypatch.setattr(requests, "post", fake_post_lookup_error)
    # A missing key should cause a KeyError which is a subclass of LookupError
    with pytest.raises(LookupError):
        generate_gemini_response("Test prompt")

def test_generate_gemini_response_request_payload(monkeypatch):
    # This test captures the payload passed to the requests.post call
    captured = {}

    def fake_post(url, headers, json):
        captured["url"] = url
        captured["headers"] = headers
        captured["json"] = json
        return FakeResponse({
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {"text": "Payload test response"}
                        ]
                    }
                }
            ]
        }, 200)

    monkeypatch.setattr(requests, "post", fake_post)
    prompt = "Test payload"
    response = generate_gemini_response(prompt)
    # Verify that the returned text is as expected
    assert response == "Payload test response"  
    # Verify that the payload contains the correct prompt
    assert captured["json"]["contents"][0]["parts"][0]["text"] == prompt
