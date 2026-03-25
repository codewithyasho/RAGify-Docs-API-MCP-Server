from fastapi import FastAPI
from pydantic import BaseModel, Field
from main import main

app = FastAPI()


# schema for user input
class UserInput(BaseModel):
    url: str = Field(..., description="The URL of the Documentation to scrape")
    query: str = Field(...,
                       description="The question to ask about the scraped content")


@app.get("/")
def home():
    return {"message": "Welcome to the RAGify Docs API. Use the /ragify endpoint to ask questions about documentation from a given URL."}


@app.get("/about")
def about():
    return {
        "name": "RAGify Docs API",
        "description": "An API that scrapes documentation from a given URL and answers questions using a Retrieval-Augmented Generation (RAG) system built with LangChain and Ollama.",
        "author": "Yashodeep",
        "version": "1.0"
    }


@app.post("/ragify")
def ragify(user_input: UserInput):
    # Initialize the RAG system
    url = user_input.url
    rag_chain = main(url)

    # Invoke the RAG chain with the user's query
    response = rag_chain.invoke({"input": user_input.query})

    return {
        "answer": response["answer"],
        "sources": [doc.metadata.get("source") for doc in response["context"]]
    }
