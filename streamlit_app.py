import os
import streamlit as st
from dotenv import load_dotenv

from app.graph import build_graph
from app.rag_pdf import ingest_pdf

load_dotenv()

st.set_page_config(page_title="AI Pipeline Demo", page_icon="☁️", layout="wide")
st.title("AI Engineer Assignment – Weather + PDF RAG (LangGraph)")

# Sidebar: PDF ingest + keys status
with st.sidebar:
st.header("Data & Settings")
pdf_file = st.file_uploader("Upload a PDF to (re)index", type=["pdf"])
if pdf_file:
pdf_path = os.path.join("data", "uploaded.pdf")
os.makedirs("data", exist_ok=True)
with open(pdf_path, "wb") as f:
f.write(pdf_file.read())
n = ingest_pdf(pdf_path)
st.success(f"Ingested {n} chunks from uploaded PDF.")

st.write("---")
st.caption("Env status")
st.write("OpenWeather API:", "" if os.getenv("OPENWEATHER_API_KEY") else "")
st.write("OpenAI API:", "" if os.getenv("OPENAI_API_KEY") else "")
st.write("LangSmith:", "" if os.getenv("LANGCHAIN_API_KEY") else "")

if "graph" not in st.session_state:
st.session_state.graph = build_graph()

if "history" not in st.session_state:
st.session_state.history = []

user_q = st.chat_input("Ask about weather (e.g., 'weather in Delhi') or ask about the PDF.")
if user_q:
st.session_state.history.append({"role": "user", "content": user_q})
with st.chat_message("user"):
st.markdown(user_q)

with st.chat_message("assistant"):
placeholder = st.empty()
out = st.session_state.graph.invoke({"question": user_q, "chat_history": st.session_state.history})
answer = out.get("answer", "Sorry, I couldn't produce an answer.")
placeholder.markdown(answer)
st.session_state.history.append({"role": "assistant", "content": answer})

# Show history
with st.expander("Conversation Trace"):
for m in st.session_state.history:
st.write(f"**{m['role']}**: {m['content']}")
