import logging
import requests
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise EnvironmentError("API_KEY not found in environment variables.")

# Define the API endpoint
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

def generate_gemini_response(prompt: str) -> str:
    """
    Generates a response from Gemini api using the provided prompt

    Args:
        prompt (str): The prompt provided by user

    Returns:
        str: generated response from Gemini

    Raises:
        requests.RequestException: If the API request fails
        LookupError: If there is an error parsing the Gemini's response
    """

    # Set the headers
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "system_instruction": {
            "parts": [
                {"text": "You are an assistant that extracts flight details from user queries"}
            ]
        },
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig":{
            "temperature": 0 # So the output doesn't varies minmally
        }
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        data = response.json()
        
        # extracts just the bots response
        return data["candidates"][0]["content"]["parts"][0]["text"]
    
    except requests.RequestException as api_err:
        logging.error(f"Error calling Gemini API: {api_err}")
        raise
    except LookupError as parse_err:
        logging.error(f"Error parsing API    response: {parse_err}")
        raise