# I Built an AI Assistant That Reads Documentation So I Do Not Have To

*How I turned any docs URL into a source-grounded Q&A service using RAG, FastAPI, and MCP*

Read time: 8-10 minutes

---

I did not build this project because AI was trending.
I built it because I was tired.

Tired of opening 20 documentation tabs.
Tired of searching the same docs three different ways.
Tired of finding half-answers in one page and key details hidden in another.

If you are a developer, you already know this loop:

- Search in docs
- Open a page
- Scroll
- Back
- Open another page
- Forget what the first page said
- Repeat

At some point, I asked myself a simple question:

What if I could just give a docs URL, ask my question in plain English, and get one grounded answer with sources?

That question became this project: **RAGify Docs API**.

---

## The Problem Was Not "No Information"

Most developer docs are good.
The real problem is fragmentation.

Information is spread across:

- Getting started pages
- API references
- Guides
- Migration notes
- FAQ pages
- Nested links three levels deep

Traditional keyword search helps, but it still makes you manually connect the dots.
Pure LLM answers are fast, but without retrieval they can hallucinate or miss project-specific details.

I wanted both:

- Speed of AI answers
- Reliability of real documentation context

That is exactly where Retrieval-Augmented Generation (RAG) fits.

---

## What RAGify Docs Actually Does

At a high level, RAGify Docs turns any documentation site into a queryable knowledge layer.

You provide:

- `url`: root docs URL
- `query`: your question

You get back:

- `answer`: generated response grounded in retrieved docs chunks
- `sources`: list of relevant documentation URLs used for the answer

So instead of "trust me" responses, you get traceable answers.

---

## The Architecture (Simple by Design)

I split the project into three focused parts:

1. **main.py** - Core RAG pipeline
2. **app.py** - FastAPI interface (`/ragify` endpoint)
3. **mcp_server.py** - MCP tool interface (`ask_docs`)

That separation ended up being one of the best design decisions.
I can improve the core pipeline once and every interface benefits.

---

## Inside the Core RAG Pipeline

Here is the flow inside `main.py`:

### 1) Recursive scraping

I use a recursive URL loader to crawl documentation pages from a root URL.
Text extraction is handled with BeautifulSoup, and noisy formatting is normalized.

### 2) Chunking for retrieval

Scraped text is split into chunks (`chunk_size=1000`, `chunk_overlap=200`).
This keeps context meaningful while making search efficient.

### 3) Embeddings + vector store

Each chunk is embedded using `sentence-transformers/all-MiniLM-L6-v2`.
Embeddings are stored in an in-memory vector store.

### 4) Retrieval strategy

I use Max Marginal Relevance (MMR) with:

- `k=5`
- `fetch_k=10`
- `lambda_mult=0.5`

This gives relevant but also diverse context, which improves final answer quality.

### 5) Answer generation

Retrieved chunks are sent to the LLM (`ChatGroq`, model `openai/gpt-oss-120b`) through a prompt that explicitly says:

- Use provided context
- If answer is not in context, say you are not sure

That one instruction is important. It reduces confident but unsupported answers.

---

## Why Caching Changed the Experience

Without caching, every question could trigger expensive re-processing.
That would be painful in real use.

So both API and MCP layers keep a URL-level cache:

- First query on a new docs URL: scrape + embed + build chain
- Next queries on same URL: reuse existing chain

This makes follow-up questions feel much faster and more conversational.

---

## API Layer: FastAPI for Product Integrations

I exposed the service through FastAPI so it is easy to integrate with web apps, bots, and internal tools.

Endpoint:

- `POST /ragify`

Request body:

```json
{
  "url": "https://docs.langchain.com/oss/python/langchain/overview",
  "query": "What is LangChain?"
}
```

Response shape:

```json
{
  "answer": "...",
  "sources": ["https://..."]
}
```

This keeps the interface minimal and production-friendly.

---

## MCP Layer: AI Agents Can Use It As a Tool

I also added an MCP server via `fastmcp`.

Tool name:

- `ask_docs(url, query)`

This lets AI clients call documentation Q&A as a structured external tool instead of guessing from static model memory.

For me, this was the most exciting part:
RAGify is not just another API. It is a tool that can plug into AI agent workflows.

---

## What I Learned While Building It

### 1) Scope control beats complexity

I avoided premature complexity like distributed vector DB setup at the start.
In-memory storage plus cache was enough to validate real usefulness.

### 2) Source attribution builds trust instantly

Users trust answers more when they can see source links.
Even a great answer feels better when verifiable.

### 3) Separation of concerns made iteration fast

Keeping core RAG logic separate from API and MCP layers made changes safer and easier.

### 4) Good prompting is a reliability feature

Prompt instructions like "if not in context, say unsure" are not optional polish.
They are core behavior control.

---

## Tradeoffs and Current Limits

This version is intentionally practical, not perfect.

Current tradeoffs:

- In-memory vector store means no persistence across restarts
- Very large doc sites can take time on first scrape
- Cache is process-local
- No auth/rate limiting yet in API layer

These are known limits, not surprises.
I wanted to ship useful first, then harden.

---

## What I Would Build Next

If I continue this in the next iteration, priorities are:

1. Persistent vector storage
2. Incremental re-indexing for docs updates
3. Better filtering controls (path/domain constraints)
4. Auth + rate limits for public deployment
5. Streaming answers for better UX

---

## Why This Pattern Matters

This project is not only about documentation.
It is a reusable pattern for any domain where:

- Information is spread across many pages
- Accuracy matters
- Users ask natural language questions

Developer docs are just the most obvious and painful use case.

---

## If You Want to Build Something Similar

Start simple:

- One source type (documentation URLs)
- One retrieval pipeline
- One minimal endpoint
- One trust mechanism (source citations)

Then optimize based on real usage.
Do not over-architect before real query patterns show up.

---

## Final Thought

The biggest win was not "better AI".
The biggest win was reducing context-switching.

Less tab-hopping.
Less manual searching.
Faster validated answers.

That is what this project gave me.

If you are building dev tools, internal copilots, or team knowledge assistants, documentation-first RAG is a great place to start.

---

## Optional Add-ons Before Publishing on Medium

To make this post even stronger on Medium, add these three things:

1. A screenshot of your README/problem statement
2. One architecture diagram image
3. One real terminal/API response screenshot

Those visuals make the story feel real and improve reading retention.

---

## Short CTA You Can Use

If this project sounds useful, I can publish a follow-up with:

- full architecture diagram
- deployment checklist
- cost/performance tuning notes
- production hardening steps

If you want that next article, tell me and I will write it.
