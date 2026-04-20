# run ingestion.py before main.py to populate your Pinecone index with embedded chunks from the source document.
import os
from operator import itemgetter

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from pinecone import Pinecone

load_dotenv()

EMBEDDING_MODEL = "gemini-embedding-001"
CHAT_MODEL = "gemini-2.5-flash"
INDEX_NAME = os.environ["INDEX_NAME"]
TOP_K = 4

print("Initializing components…")

embeddings = GoogleGenerativeAIEmbeddings(
    model=EMBEDDING_MODEL,
    google_api_key=os.environ["GOOGLE_API_KEY"],
)

llm = ChatGoogleGenerativeAI(
    model=CHAT_MODEL,
    google_api_key=os.environ["GOOGLE_API_KEY"],
    temperature=0.2,
)

pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
index = pc.Index(INDEX_NAME)

prompt_template = ChatPromptTemplate.from_template(
    """You are a knowledgeable assistant. Answer the question using ONLY the
context provided below. If the answer is not in the context, say so clearly.

Context:
{context}

Question: {question}

Answer:"""
)



# Retrieval helpers

def retrieve_docs(query: str) -> list[Document]:
    """Embed the query and search Pinecone; return a list of LangChain Documents."""
    query_vector = embeddings.embed_query(query)
    results = index.query(vector=query_vector, top_k=TOP_K, include_metadata=True)
    docs = []
    for match in results.get("matches", []):
        text = match["metadata"].get("text", "")
        meta = {k: v for k, v in match["metadata"].items() if k != "text"}
        docs.append(Document(page_content=text, metadata=meta))
    return docs


def format_docs(docs: list[Document]) -> str:
    return "\n\n".join(doc.page_content for doc in docs)


# Implementation 2 — LCEL chain
#PLACEHOLDER# build_rag_chain



if __name__ == "__main__":
    query = "What storage options does Proxmox support and which is best for a home lab?"

    # Option 0 — raw LLM (no RAG, no context)
    #PLACEHOLDER#
  

  


   
    # Option 2 — LCEL chain
    print("\n" + "=" * 70)
    print("OPTION 2: RAG with LCEL chain")
    print("=" * 70)
    #PLACEHOLDER#


