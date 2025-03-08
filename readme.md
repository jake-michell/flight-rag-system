# Flight Retrieval-Augmented Generation (RAG) System

## Features
- Mock database of flights 60+ flights
- Can answer users questions using relevant flight information
- Uses Gemini API for intelligent reasoning and responses
- Docker containerization for easy deployment

## Requirements
- Docker version 27.5.1
- Docker Compose version v2.32.4
- Gemini api key
---
## Setup
1. Clone the repository:

```bash
git clone https://github.com/jake-michell/flight-rag-system.git
cd flight-rag-system
```
2. Setup environment variables
```bash
echo "API_KEY=your_gemini_api_key_here" > .env
```

3. Build and run
```bash
docker-compose run --rm flight_rag
```
---
## usage
```bash
Enter your flight query: flights to new york
DEBUG:urllib3.connectionpool:Starting new HTTPS connection (1): generativelanguage.googleapis.com:443
DEBUG:urllib3.connectionpool:https://generativelanguage.googleapis.com:443 "POST /v1beta/models/gemini-2.0-flash:generateContent?key=AIzaSyBSV4sef3hnrsYjSFPBuTQl0K2EvxG87d4 HTTP/1.1" 200 None
{
    "flight_number": null,
    "origin": null,
    "destination": "new york",
    "date": null,
    "time": null,
    "before_date": null,
    "after_date": null,
    "before_time": null,
    "after_time": null
}
INFO:root:
 Parameters:
 {'after_date': None,
 'after_time': None,
 'before_date': None,
 'before_time': None,
 'date': None,
 'destination': 'new york',
 'flight_number': None,
 'origin': None,
 'time': None}
INFO:root:
Flights Found:
 [{'date': datetime.date(2025, 3, 3),
  'destination': 'New York',
  'flight_number': 'BA202',
  'origin': 'London',
  'time': datetime.time(10, 0)},
 {'date': datetime.date(2025, 3, 3),
  'destination': 'New York',
  'flight_number': 'LH505',
  'origin': 'Frankfurt',
  'time': datetime.time(12, 0)},
 {'date': datetime.date(2025, 3, 5),
  'destination': 'New York',
  'flight_number': 'AI1313',
  'origin': 'Delhi',
  'time': datetime.time(5, 40)},
 {'date': datetime.date(2025, 3, 6),
  'destination': 'New York',
  'flight_number': 'TK1717',
  'origin': 'Istanbul',
  'time': datetime.time(22, 30)},
 {'date': datetime.date(2025, 3, 3),
  'destination': 'New York',
  'flight_number': 'EK2222',
  'origin': 'Dubai',
  'time': datetime.time(2, 45)}]
DEBUG:urllib3.connectionpool:Starting new HTTPS connection (1): generativelanguage.googleapis.com:443
DEBUG:urllib3.connectionpool:https://generativelanguage.googleapis.com:443 "POST /v1beta/models/gemini-2.0-flash:generateContent?key=AIzaSyBSV4sef3hnrsYjSFPBuTQl0K2EvxG87d4 HTTP/1.1" 200 None
  Here are the flights to New York that I found:
    - BA202 from London on March 3, 2025 at 10:00 AM
    - LH505 from Frankfurt on March 3, 2025 at 12:00 PM
    - AI1313 from Delhi on March 5, 2025 at 5:40 AM
    - TK1717 from Istanbul on March 6, 2025 at 10:30 PM
    - EK2222 from Dubai on March 3, 2025 at 2:45 AM
```
Examples Queries:
- "List flights after 2pm today"
- "Show me flights from london to new york"
- "Show me flights to San Francisco from the 6th to the 7th"
- "Quel est le vol le plus tôt de New York à Londres le 5 mars 2025 ?"

## Project Structure
```
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
├── mock_database.py      # Mock flight data
├── query_handler.py      # Handles users questions
├── gemini_api.py         # API integration
├── utils.py              # Helper functions
├── main.py               # CLI interface
└── tests/                # Comprehensive test suite
```
