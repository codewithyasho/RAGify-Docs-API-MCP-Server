import os
from fastmcp import FastMCP
from main import main

mcp = FastMCP(
    name="RAGify Docs MCP Server"
)

rag_cache = {}


@mcp.tool(
    name="ask_docs",
    description="Ask questions about any documentation website by providing a URL and a question."
)
def ask_docs(url: str, query: str):
    try:
        # 🔥 Cache
        if url not in rag_cache:
            rag_cache[url] = main(url)

        rag_chain = rag_cache[url]

        response = rag_chain.invoke({"input": query})

        # ✅ Return structured response
        return {
            "answer": response["answer"],
            "sources": list(set(
                doc.metadata.get("source")
                for doc in response["context"]
                if doc.metadata.get("source")
            ))
        }

    except Exception as e:
        return {
            "error": str(e)
        }


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))

    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=port
    )
