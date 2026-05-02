import os
from dotenv import load_dotenv
from serpapi import GoogleSearch

load_dotenv()

SERP_API_KEY = os.getenv("SERPAPI_API_KEY")


def search_tool(state):
    query = state.get("question", "")

    if not query:
        return {
            "question": "",
            "retriever": state.get("retriever"),
            "search_results": ""
        }

    params = {
        "q": query,
        "api_key": SERP_API_KEY,
        "num": 3
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    snippets = []
    for r in results.get("organic_results", []):
        snippet = r.get("snippet", "")
        if snippet:
            snippets.append(snippet)

    print("\n[SEARCH RESULTS]:\n", "\n".join(snippets))

    return {
    "question": query,
    "retriever": state.get("retriever"),
    "route": state.get("route"),  # ✅ ADD THIS
    "search_results": "\n".join(snippets)
}