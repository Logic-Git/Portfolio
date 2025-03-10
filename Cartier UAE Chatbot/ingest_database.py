import os
import glob
from uuid import uuid4
from config import (
    KNOWLEDGE_BASE_DIR,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    COLLECTION_NAME,
    CHROMA_PERSIST_DIR,
)
from embeddings import get_embedding
import chromadb
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings


def load_documents(directory):
    documents = []
    for filepath in glob.glob(os.path.join(directory, "*.txt")):
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
            documents.append({"content": text, "source": filepath})
    return documents


def chunk_text(text, chunk_size, chunk_overlap):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - chunk_overlap
    return chunks


def index_documents():
    # Load raw documents from the knowledge base directory.
    raw_docs = load_documents(KNOWLEDGE_BASE_DIR)
    print(f"Loaded {len(raw_docs)} documents.")

    # Initialize ChromaDB client with persistence.
    client = chromadb.PersistentClient(
        path=CHROMA_PERSIST_DIR,
        settings=Settings(),
        tenant=DEFAULT_TENANT,
        database=DEFAULT_DATABASE,
    )
    # Create or retrieve the collection.
    try:
        collection = client.get_collection(name=COLLECTION_NAME)
    except Exception:
        collection = client.create_collection(name=COLLECTION_NAME)

    all_chunks = []
    ids = []
    metadatas = []

    for doc in raw_docs:
        chunks = chunk_text(doc["content"], CHUNK_SIZE, CHUNK_OVERLAP)
        for chunk in chunks:
            all_chunks.append(chunk)
            ids.append(str(uuid4()))
            metadatas.append({"source": doc["source"]})

    # Generate embeddings for each chunk using Gemini.
    embeddings = [get_embedding(chunk) for chunk in all_chunks]

    # Add documents to the ChromaDB collection.
    collection.add(
        documents=all_chunks, embeddings=embeddings, metadatas=metadatas, ids=ids
    )
    print(
        f"Indexed {len(all_chunks)} chunks into ChromaDB collection '{COLLECTION_NAME}'."
    )


if __name__ == "__main__":
    index_documents()
