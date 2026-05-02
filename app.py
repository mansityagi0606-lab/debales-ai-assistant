import os
from dotenv import load_dotenv

from scraper import scrape_website
from rag import create_vectorstore
from tools import search_tool
from graph import build_graph

load_dotenv()

# Step 1: Scrape
print("Scraping data...")
texts = scrape_website()

# Step 2: Vector DB
print("Creating vectorstore...")
vectorstore = create_vectorstore(texts)
retriever = vectorstore.as_retriever()

# Step 3: Graph
app = build_graph()

print("\nDebales AI Assistant Ready!\n")

# Step 4: CLI loop
while True:
    query = input("Ask: ")

    if query.lower() in ["exit", "quit"]:
        break

    result = app.invoke({
        "question": query,
        "retriever": retriever
    })

    print("\nAnswer:", result["answer"])
    print("-" * 50)