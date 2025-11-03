from typing import TypedDict, Literal, List
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from .llm import get_llm
from .rag_pdf import rag_answer, ingest_pdf
from .weather import weather_answer

# ---- State ----
class State(TypedDict, total=False):
question: str
intent: Literal["weather", "rag"]
answer: str
chat_history: List[dict]

# ---- Router ----
WEATHER_HINTS = ("weather", "temperature", "forecast", "rain", "sunny", "cold", "hot")

def route(state: State) -> Literal["weather", "rag"]:
q = (state.get("question") or "").lower()
if any(w in q for w in WEATHER_HINTS):
return "weather"
# also route when user mentions "in <city>"
if " in " in f" {q} ":
return "weather"
return "rag"

# ---- Nodes ----
def classify_node(state: State) -> State:
state["intent"] = route(state)
return state

def weather_node(state: State) -> State:
state["answer"] = weather_answer(state["question"])
return state

def rag_node(state: State) -> State:
llm = get_llm()
state["answer"] = rag_answer(state["question"], llm)
return state

# ---- Build graph ----
def build_graph():
# Try ingest once at startup (ignores if no PDF present)
try:
ingest_pdf()
except Exception:
pass

g = StateGraph(State)
g.add_node("classify", classify_node)
g.add_node("weather", weather_node)
g.add_node("rag", rag_node)

g.add_edge("classify", "weather") # default, but we'll override with conditional
g.set_entry_point("classify")
g.add_conditional_edges("classify", lambda s: s["intent"], {
"weather": "weather",
"rag": "rag",
})
g.add_edge("weather", END)
g.add_edge("rag", END)

memory = MemorySaver()
return g.compile(checkpointer=memory)