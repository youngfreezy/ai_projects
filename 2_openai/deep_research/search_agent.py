from pydantic import BaseModel

class WebSearchItem(BaseModel):
    query: str
    reason: str

class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem]

from openai import OpenAI

INSTRUCTIONS = """You are a research assistant performing a web search. For each search:
1. Find the most relevant and recent information
2. Include specific facts, statistics, and data when available
3. Note any conflicting viewpoints or debates
4. Cite sources or experts when possible
5. Focus on verified information from reputable sources"""