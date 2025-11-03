import os
from langchain_openai import ChatOpenAI

def get_llm():
# Small, cheap, deterministic LLM for routing/answering
return ChatOpenAI(model="gpt-4o-mini", temperature=0.2)