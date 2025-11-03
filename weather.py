

import os, re, requests

OWM_KEY = os.getenv("OPENWEATHER_API_KEY")

CITY_PAT = re.compile(r"(?:in|at|for)\s+([A-Za-z][A-Za-z\s\-]+)$", re.IGNORECASE)

def extract_city(q: str) -> str | None:
m = CITY_PAT.search(q.strip())
if m:
return m.group(1).strip()
# naive fallbacks
tokens = q.lower().split()
if "in" in tokens:
idx = tokens.index("in")
return " ".join(q.split()[idx+1:]).strip() or None
return None

def fetch_weather(city: str) -> dict:
if not OWM_KEY:
raise RuntimeError("OPENWEATHER_API_KEY not set")
url = "https://api.openweathermap.org/data/2.5/weather"
params = {"q": city, "appid": OWM_KEY, "units": "metric"}
r = requests.get(url, params=params, timeout=10)
r.raise_for_status()
return r.json()

def format_weather(data: dict) -> str:
name = data.get("name")
main = data.get("weather", [{}])[0].get("description", "N/A").title()
temp = data.get("main", {}).get("temp", "N/A")
feels = data.get("main", {}).get("feels_like", "N/A")
hum = data.get("main", {}).get("humidity", "N/A")
wind = data.get("wind", {}).get("speed", "N/A")
return f"Weather in **{name}**: {main}. Temp: {temp}°C (feels {feels}°C), Humidity: {hum}%, Wind: {wind} m/s."

def weather_answer(question: str) -> str:
city = extract_city(question) or "Delhi"
data = fetch_weather(city)
return format_weather(data)