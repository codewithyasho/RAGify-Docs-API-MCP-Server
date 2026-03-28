# 📚 RAGify Docs API

<div align="center">

**A Developer's Tool for Interactive Documentation**

Scrape entire documentation recursively and ask AI-powered questions using Retrieval-Augmented Generation (RAG)

![Python](https://img.shields.io/badge/Python-3.12+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.135+-green)
![LangChain](https://img.shields.io/badge/LangChain-1.2+-orange)
![Groq](https://img.shields.io/badge/Groq-API-blueviolet)
![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-lightgrey)

</div>

---

## 🎯 Overview

**RAGify Docs** is a comprehensive tool that helps developers quickly navigate and understand documentation by combining web scraping, vector embeddings, and AI-powered question answering. Instead of manually reading through documentation, simply provide a URL and ask questions—RAGify will find the most relevant answers backed by actual documentation content.

### ✨ Key Features

- 🕷️ **Recursive Web Scraping** - Automatically traverse and extract content from entire documentation websites
- 🧠 **Vector Embeddings** - Convert documentation into semantic embeddings using HuggingFace models
- 🎯 **Smart Retrieval** - Use Max Marginal Relevance (MMR) to fetch diverse and relevant context
- 🤖 **AI-Powered Answers** - Leverage Groq's fast language models for accurate responses
- ⚡ **Intelligent Caching** - Reuse embeddings across multiple queries on the same documentation
- 🔌 **Multiple Interfaces** - Access via REST API, MCP Server, or direct Python module
- 📍 **Source Attribution** - Get links to the exact documentation pages used to answer your questions
- 🚀 **Production-Ready** - Built with FastAPI and async support for scalable deployments

---

## 🏗️ Project Structure

```
RAGify-Docs-API/
├── main.py              # Core RAG engine - documentation scraping & question answering
├── app.py               # FastAPI REST API server
├── mcp_server.py        # MCP (Model Context Protocol) server for Claude/AI integrations
├── pyproject.toml       # Project metadata and dependencies
├── requirements.txt     # Python package requirements
└── README.md            # This file
```

### Component Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    RAGify Docs API                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐  │
│  │  FastAPI     │  │  MCP Server  │  │   Python    │  │
│  │  (/ragify)   │  │ (ask_docs)   │  │   Module    │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬──────┘  │
│         │                 │                  │         │
│         └─────────────────┼──────────────────┘         │
│                           │                           │
│                    ┌──────▼───────┐                   │
│                    │   main.py    │                   │
│                    │  (RAG Core)  │                   │
│                    └──────┬───────┘                   │
│                           │                           │
│         ┌─────────────────┼─────────────────┐         │
│         │                 │                 │         │
│    ┌────▼────┐      ┌─────▼──────┐   ┌────▼─────┐  │
│    │ Scraper │      │ Embeddings │   │    LLM   │  │
│    │ (URL)   │      │  (HF)      │   │  (Groq) │  │
│    └────┬────┘      └─────┬──────┘   └────┬─────┘  │
│         │                 │                │       │
│         └─────────────────┼────────────────┘       │
│                           │                        │
│                    ┌──────▼────────┐              │
│                    │ Cache Storage │              │
│                    │    (In-Mem)   │              │
│                    └───────────────┘              │
│                                                   │
└─────────────────────────────────────────────────────┘
```

---

## 🚀 Installation

### Prerequisites

- Python 3.12+
- pip or uv package manager
- API keys for Groq (optional alternative: use Ollama locally)

### Setup Steps

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd RAGify-Docs-API
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # or
   source .venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   # or using uv
   uv sync
   ```

4. **Create a `.env` file** (Optional - for API keys)

   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

---

## 📖 Usage

### Option 1: FastAPI REST API

**Start the server:**

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

**Make a request:**

```bash
curl -X POST "http://localhost:8000/ragify" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://docs.langchain.com/oss/python/langchain/overview",
    "query": "What is LangChain?"
  }'
```

**Python example:**

```python
import requests

response = requests.post(
    "http://localhost:8000/ragify",
    json={
        "url": "https://docs.python.org/3/",
        "query": "How do I create a list?"
    }
)

print(response.json())
# {
#     "answer": "...",
#     "sources": ["https://docs.python.org/3/..."]
# }
```

**API Documentation:**

- Interactive docs: `http://localhost:8000/docs` (Swagger UI)
- ReDoc: `http://localhost:8000/redoc`

---

### Option 2: MCP Server

**Start the MCP server:**

```bash
python mcp_server.py
```

Default configuration:

- Host: `0.0.0.0`
- Port: `8000` (or from `PORT` env variable)
- Transport: HTTP Streamable

---

### Option 3: Direct Python Module

**Use RAGify in your own Python code:**

```python
from main import main

# Initialize RAG for a documentation URL
rag_chain = main("https://docs.langchain.com/oss/python/langchain/overview")

# Ask questions
response = rag_chain.invoke({
    "input": "What is a retriever in LangChain?"
})

print(response["answer"])
print(response["context"])  # List of source documents
```

---

## 🔑 Configuration

### Environment Variables

```env
# Groq API Configuration
GROQ_API_KEY=your_key_here
GROQ_MODEL=openai/gpt-oss-120b

# Or use Ollama instead of Groq (local inference)
# Uncomment in main.py: llm = ChatOllama(model="your-model")

# MCP Server Port
PORT=8000
```

### Customization in `main.py`

**Chunk size and overlap:**

```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # Increase for longer contexts
    chunk_overlap=200     # Increase for better continuity
)
```

**Embedding model:**

```python
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
    # Or use: "all-mpnet-base-v2" (larger, more accurate)
)
```

**Retrieval parameters:**

```python
retriever = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 5,           # Number of results to return
        "fetch_k": 10,    # Candidates to consider
        "lambda_mult": 0.5 # Balances similarity vs diversity
    }
)
```

**LLM selection:**

```python
# Use Groq (fast, requires API key)
llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0.2)

# OR use Ollama locally (no API key needed)
# llm = ChatOllama(model="llama2", temperature=0.2)
```

---

## 📋 API Reference

### FastAPI Endpoints

#### `POST /ragify`

Ask a question about documentation.

**Request:**

```json
{
  "url": "https://docs.example.com",
  "query": "How do I get started?"
}
```

**Response:**

```json
{
  "answer": "To get started with Example...",
  "sources": [
    "https://docs.example.com/getting-started",
    "https://docs.example.com/installation"
  ]
}
```

**Status Codes:**

- `200` - Success
- `500` - RAG initialization or invocation error

---

#### `GET /`

Health check and welcome message.

**Response:**

```json
{
  "message": "Welcome to the RAGify Docs API! Use the /ragify endpoint to ask questions about documentation."
}
```

---

### MCP Tool: `ask_docs`

Accessible through MCP clients (Claude, etc.)

**Parameters:**

- `url` (string): Documentation URL to scrape
- `query` (string): Question to ask

**Returns:**

```json
{
  "answer": "...",
  "sources": ["url1", "url2"]
}
```

Or on error:

```json
{
  "error": "Error message"
}
```

---

## 🚀 Deployment

### Docker (Optional)

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Build and run:**

```bash
docker build -t ragify-docs-api .
docker run -p 8000:8000 -e GROQ_API_KEY=your_key ragify-docs-api
```

---

<div align="center">

**Built with ❤️ for developers who love great documentation**

⭐ If you found this useful, please star the repository!

</div>
