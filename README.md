# AI Research Assistant

A production-ready Retrieval-Augmented Generation (RAG) pipeline with a lightweight intelligent routing layer. Users can upload PDFs, ask questions based on the document's contents, or ask for a comprehensive summary.

## Architecture

![Architecture Strategy](./walkthrough.md) *(See Walkthrough for architecture)*

- **Backend:** FastAPI (Python)
- **Embeddings:** `all-MiniLM-L6-v2` via `sentence-transformers`
- **Vector Store:** FAISS (`faiss-cpu`) local in-memory index + JSON metadata
- **LLM:** `llama-3.3-70b-versatile` via Groq Free Tier API
- **Agent/Router:** Deterministic intent classifier for Q&A vs Summarize modes
- **Frontend:** React + Vite + Vanilla CSS Glassmorphism

## Prerequisites

- [Groq API Key (Free)](https://console.groq.com)
- Python 3.9+
- Node.js & npm (for running the frontend locally)

## Local Setup

### 1. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the `backend` directory:
```
GROQ_API_KEY=your_groq_api_key_here
```

Start the backend:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
*API docs will be available at http://localhost:8000/docs*

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

*The App will be available at http://localhost:5173*

## Deployment

### Render (Backend)
The backend is configured for the Render Free Tier.
1. Connect this repo to Render.
2. Create a "Web Service" from the `backend/render.yaml` configuration.
3. Once deployed, add your `GROQ_API_KEY` into the Environment settings on the Render Dashboard.

*Note: The free tier spins down after 15 mins of inactivity, which may cause 30-60 second cold starts and embedding delays.*

### Vercel (Frontend)
1. Import the `/frontend` directory as a new Project in Vercel.
2. Set the Framework Preset to Vite.
3. Add the `VITE_API_URL` environment variable pointing to your deployed Render backend (e.g., `https://rag-research-assistant.onrender.com`).
4. The `vercel.json` ensures client-side routing works properly.

## Design Decisions
- **Deterministic Agent Routing:** A regex/keyword-based router is used instead of a heavy LangChain ReAct agent. It runs securely offline without LLM latency for the routing step.
- **Glassmorphism UI:** Built with raw CSS to ensure no dependency bloat, fulfilling the robust aesthetics requirement. 
- **Offline Indexing:** Extracting & embedding the chunks ensures the LLM is only called during inference.
