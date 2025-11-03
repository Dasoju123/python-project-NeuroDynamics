from app.graph import route

def test_route_weather_keywords():
assert route({"question": "Give me the weather in Pune"}) == "weather"
assert route({"question": "temperature today"}) == "weather"

def test_route_rag_default():
assert route({"question": "Summarize section 2"}) == "rag"