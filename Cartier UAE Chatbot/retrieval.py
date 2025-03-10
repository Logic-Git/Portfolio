import chromadb
from chromadb.config import Settings, DEFAULT_TENANT, DEFAULT_DATABASE
from config import COLLECTION_NAME, CHROMA_PERSIST_DIR, MAX_RESULTS
from embeddings import get_embedding


def query_knowledge(query_text: str, n_results: int = MAX_RESULTS):
    # Initialize the ChromaDB client with the same configuration as ingest_database.py
    client = chromadb.PersistentClient(
        path=CHROMA_PERSIST_DIR,
        settings=Settings(),
        tenant=DEFAULT_TENANT,
        database=DEFAULT_DATABASE,
    )
    try:
        collection = client.get_collection(name=COLLECTION_NAME)
    except Exception as e:
        print("Error: The knowledge base hasn't been initialized yet.")
        print(
            "Please run 'python ingest_database.py' first to initialize the knowledge base."
        )
        return []

    # Generate the query embedding using Gemini.
    query_embedding = get_embedding(query_text)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["documents", "metadatas"],
    )
    # Extract and return the top documents.
    docs = results["documents"][0]
    return docs
