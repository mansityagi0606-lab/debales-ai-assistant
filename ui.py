import streamlit as st
from scraper import scrape_website
from rag import create_vectorstore
from graph import build_graph

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Debales AI Assistant", layout="wide")

st.title("🤖 Debales AI Assistant")
st.markdown("Ask anything about Debales AI or general topics.")

# ---------------- LOAD APP ----------------
@st.cache_resource
def setup_app():
    texts = scrape_website()
    vectorstore = create_vectorstore(texts)
    retriever = vectorstore.as_retriever()
    app = build_graph()
    return app, retriever

app, retriever = setup_app()

# ---------------- SESSION STATE ----------------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- BADGE FUNCTION ----------------
def get_badge(route):
    route = route.lower()
    if route == "rag":
        return "🟢 **RAG**"
    elif route == "search":
        return "🔵 **SEARCH**"
    elif route == "both":
        return "🟣 **BOTH**"
    else:
        return "⚪ UNKNOWN"

# ---------------- INPUT ----------------
query = st.text_input("Ask your question:")

if st.button("Submit") and query:
    with st.spinner("Thinking..."):
        result = app.invoke({
            "question": query,
            "retriever": retriever
        })

        answer = result.get("answer", "")
        route = result.get("route", "unknown")  # 👈 IMPORTANT

        st.session_state.history.append({
            "question": query,
            "answer": answer,
            "route": route
        })

# ---------------- DISPLAY ----------------
for item in reversed(st.session_state.history):
    st.markdown(f"**🧑 You:** {item['question']}")
    
    # ✅ ROUTE BADGE
    badge = get_badge(item["route"])
    st.markdown(f"{badge}")
    
    st.markdown(f"**🤖 Bot:** {item['answer']}")
    st.markdown("---")