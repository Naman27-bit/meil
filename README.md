# Restaurant Review Q&A (Pizza)

A small RAG (Retrieval-Augmented Generation) app that answers questions about a pizza restaurant using:
- **Vector search** over review text (stored in **Chroma**)
- **Ollama** models (LLM + embeddings)

A **Streamlit** UI lets you chat with the system.

---

## Project structure

- `vector.py` - builds/loads the Chroma vector database from `realistic_restaurant_reviews.csv`
- `main.py` - retrieves relevant reviews and asks the LLM to answer
- `frontend/streamlit_app.py` - Streamlit chat interface
- `realistic_restaurant_reviews.csv` - dataset of pizza restaurant reviews
- `chrome_langchain_db/` - persisted Chroma database

---

## Prerequisites

1. **Python 3.10+**
2. **Ollama** running locally
3. Pull the required Ollama models:
   - LLM: `llama3.2`
   - Embeddings: `mxbai-embed-large`

---

## Setup

### 1) Install dependencies

```bash
pip install -r requirements.txt
```

### 2) Ensure the CSV path works

`vector.py` loads `realistic_restaurant_reviews.csv` from the project root. Run the app from the repo root.

---

## Run the app

### Start Streamlit

```bash
streamlit run frontend/streamlit_app.py
```

Open the URL shown in the terminal and ask questions like:
- “What do people say about the crust?”
- “Are there negative reviews about delivery?”
- “Do they have gluten-free options?”

---

## How it works (RAG pipeline)

1. **Indexing (one time)**: `vector.py`
   - Reads rows from the CSV
   - Creates LangChain `Document`s (title + review)
   - Stores embeddings in Chroma (`chrome_langchain_db/`)

2. **Question answering**: `main.py`
   - Uses the Chroma retriever to fetch the top **k=5** relevant reviews
   - Sends the retrieved reviews + the user question to the LLM
   - Returns the generated answer

3. **UI**: `frontend/streamlit_app.py`
   - Maintains chat history via `st.session_state`
   - Calls `get_answer(prompt)` for each user message

---

## Notes / customization

- **Top-k retrieval** is controlled here:
  - `vector.py`: `search_kwargs={"k": 5}`
- **LLM model** is controlled here:
  - `main.py`: `OllamaLLM(model="llama3.2")`
- **Embedding model** is controlled here:
  - `vector.py`: `OllamaEmbeddings(model="mxbai-embed-large")`

---

## Troubleshooting

- **Chroma DB already exists**: `vector.py` only adds documents if `./chrome_langchain_db` doesn’t exist.
  - If you change the dataset, delete `chrome_langchain_db/` and re-run.
- **Model not found**: If Ollama can’t find `llama3.2` or `mxbai-embed-large`, pull them in Ollama.

# tanushree
