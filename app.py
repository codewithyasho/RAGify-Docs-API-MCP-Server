from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from main import main

# ========== Initialize FastAPI ==========
app = FastAPI(
    title="RAGify Docs API",
    description="A comprehensive API for RAGify Docs, allowing users to scrape documentation from a given URL and ask questions about it using a Retrieval-Augmented Generation (RAG) system built with LangChain and Groq.",
    version="1.0.0"
)

# ========== Configure CORS ==========
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)


# schema for user input
class UserInput(BaseModel):
    url: str = Field(..., description="The URL of the Documentation to scrape", examples=[
        "https://docs.langchain.com/oss/python/langchain/overview"])
    query: str = Field(...,
                       description="The question to ask about the scraped content", examples=["What is LangChain?"])


@app.get("/")
def home():
    return {"message": "Welcome to the RAGify Docs API. Use the /ragify endpoint to ask questions about documentation from a given URL."}


rag_cache = {}


@app.post("/ragify")
async def ragify(user_input: UserInput):
    try:
        url = user_input.url

        # 🔥 CACHE + ASYNC SAFE
        if url not in rag_cache:
            rag_cache[url] = await run_in_threadpool(main, url)

        rag_chain = rag_cache[url]

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"RAG init failed: {str(e)}"
        )

    try:
        response = await run_in_threadpool(
            rag_chain.invoke,
            {"input": user_input.query}
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error invoking RAG chain: {str(e)}"
        )

    return {
        "answer": response["answer"],
        "sources": list(set(doc.metadata.get("source") for doc in response["context"]))
    }
