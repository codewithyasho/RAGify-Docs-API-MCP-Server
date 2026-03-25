from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
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


@app.post("/ragify")
def ragify(user_input: UserInput):
    # Initialize the RAG system
    try:
        url = user_input.url
        rag_chain = main(url)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Error initializing RAG system")

    # Invoke the RAG chain with the user's query
    try:
        response = rag_chain.invoke({"input": user_input.query})

    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Error invoking RAG chain")

    return {
        "answer": response["answer"],
        "sources": [doc.metadata.get("source") for doc in response["context"]]
    }
