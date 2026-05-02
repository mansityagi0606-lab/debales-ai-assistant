import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph
from langchain_groq import ChatGroq

from tools import search_tool

load_dotenv()

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="openai/gpt-oss-120b"
)

# ---------------- ROUTER ----------------
def router(state):
    question = state.get("question", "")
    retriever = state.get("retriever")

    prompt = f"""
    Classify the query:
    - rag → if about Debales AI
    - search → if general knowledge
    - both → if mixed (Debales AI + general)

    Only return one word: rag, search, or both.

    Question: {question}
    """

    decision = llm.invoke(prompt).content.lower().strip()

    if "both" in decision:
        route = "both"
    elif "rag" in decision:
        route = "rag"
    else:
        route = "search"

    print("\n[ROUTER DECISION]:", route)

    return {
        "route": route,
        "question": question,
        "retriever": retriever
    }


# ---------------- RAG ----------------
def rag_node(state):
    question = state.get("question", "")
    retriever = state.get("retriever")
    route = state.get("route")

    # ✅ updated method
    docs = retriever.invoke(question)

    context = "\n".join([doc.page_content for doc in docs])

    print("\n[RAG CONTEXT]:\n", context[:500])

    return {
        "question": question,
        "retriever": retriever,
        "route": route,
        "context": context
    }


# ---------------- BOTH ----------------
def both_node(state):
    question = state.get("question", "")
    retriever = state.get("retriever")
    route = state.get("route")

    rag_result = rag_node(state)
    search_result = search_tool(state)

    print("\n[BOTH NODE USED]")

    return {
        "question": question,
        "retriever": retriever,
        "route": route,
        "context": rag_result.get("context", ""),
        "search_results": search_result.get("search_results", "")
    }


# ---------------- GENERATOR ----------------
def generator(state):
    question = state.get("question", "")
    context = state.get("context", "")
    search_results = state.get("search_results", "")
    route = state.get("route", "unknown")

    print("\n[GENERATOR INPUT]")
    print("Route:", route)
    print("Context preview:", context[:200])
    print("Search preview:", search_results[:200])

    prompt = f"""
    You are an AI assistant.

    Use ONLY the information provided below.

    Context:
    {context}

    Search Results:
    {search_results}

    Rules:
    - If both are empty → say "I don't know"
    - If context exists → prioritize it
    - If search exists → use it as support
    - Do NOT make up information
    - Be concise

    Question: {question}
    """

    answer = llm.invoke(prompt).content

    return {
        "answer": answer,
        "route": route  # ✅ IMPORTANT for UI badge
    }


# ---------------- GRAPH ----------------
def build_graph():

    graph = StateGraph(dict)

    graph.add_node("router", router)
    graph.add_node("rag", rag_node)
    graph.add_node("search", search_tool)
    graph.add_node("both", both_node)
    graph.add_node("generator", generator)

    graph.set_entry_point("router")

    graph.add_conditional_edges(
        "router",
        lambda x: x["route"],
        {
            "rag": "rag",
            "search": "search",
            "both": "both"
        }
    )

    graph.add_edge("rag", "generator")
    graph.add_edge("search", "generator")
    graph.add_edge("both", "generator")

    graph.set_finish_point("generator")

    return graph.compile()