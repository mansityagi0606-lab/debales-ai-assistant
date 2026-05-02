# Debales AI Assistant

An AI-powered chatbot built using LangGraph that can intelligently answer questions about Debales AI using RAG (Retrieval-Augmented Generation) and handle general queries using a SERP API.

---

## Features

- **RAG (Retrieval-Augmented Generation)**  
  Answers Debales AI-specific questions using scraped website data.

- **SERP API Integration**  
  Handles general queries using real-time search results.

- **Smart Routing (LangGraph)**  
  Automatically decides:
  - `RAG` → Debales AI queries  
  - `SEARCH` → General queries  
  - `BOTH` → Mixed queries  

- **No Hallucination**  
  Responds with *"I don't know"* when information is unavailable.

- **Streamlit UI**  
  Interactive chatbot interface with route badges.

---

## Tech Stack

- LangGraph
- LangChain
- Groq (LLM - LLaMA3)
- FAISS (Vector DB)
- HuggingFace Embeddings
- SerpAPI (Google Search)
- Streamlit (UI)

---

<img width="259" height="254" alt="image" src="https://github.com/user-attachments/assets/a3850d9f-12b8-4433-8432-65a284a6b722" />



---

## Setup Instructions

1) Clone the repository
Open your terminal and run:
git clone <your-repo-link>
cd debales-ai-assistant
2) Create a virtual environment
Run the following commands:
python -m venv venv
venv\Scripts\activate (For Windows)
3) Install dependencies
Install all required packages using:
pip install -r requirements.txt
4) Set up environment variables
Create a file named .env in the root directory and add the following:

  GROQ_API_KEY=your_groq_api_key
  SERPAPI_API_KEY=your_serpapi_key

5) Run the application
Start the Streamlit UI using:
streamlit run ui.py

Example Queries
RAG (Debales AI)
1) What does Debales AI do?
2) What products does Debales AI offer?
SEARCH (General)
1) What is AI in logistics?
2) What is LangGraph?
BOTH (Mixed)
1) How does Debales AI use AI in logistics?
2) Compare Debales AI with OpenAI
UNKNOWN
1) What is Debales AI revenue in 2020?
