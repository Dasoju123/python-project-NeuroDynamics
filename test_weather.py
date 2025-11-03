import json
from app.weather import extract_city, format_weather

def test_extract_city_simple():
assert extract_city("weather in Bengaluru") == "Bengaluru"
assert extract_city("What's the temperature in New York") == "New York"

def test_format_weather():
data = {
"name": "Delhi",
"weather": [{"description": "clear sky"}],
"main": {"temp": 31.2, "feels_like": 33.0, "humidity": 40},
"wind": {"speed": 3.5}
}
out = format_weather(data)
assert "Delhi" in out and "Temp:" in out