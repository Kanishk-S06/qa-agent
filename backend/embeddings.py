from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import os

# --------- Persistent Chroma Setup (Render Compatible) ---------

# Path for vector DB
CHROMA_PATH = "./chroma_data"

# Create folder if missing (important for Render & Windows)
os.makedirs(CHROMA_PATH, exist_ok=True)

# Create persistent Chroma client using new API
chroma_client = chromadb.Client(
    Settings(
        is_persistent=True,
        persist_directory=CHROMA_PATH
    )
)

# Create / load collection
collection = chroma_client.get_or_create_collection(
    name="knowledge_base",
    metadata={"hnsw:space": "cosine"}  # Recommended for sentence-transformers
)

# Load embedding model once
model = SentenceTransformer("all-MiniLM-L6-v2")


# --------- Simple splitter (no LangChain needed) ---------
def simple_splitter(text, chunk_size=400, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks


# --------- Store documents + embeddings ---------
def embed_and_store(text, metadata):
    chunks = simple_splitter(text)
    embeddings = model.encode(chunks).tolist()

    source = metadata.get("source", "doc")

    for i, chunk in enumerate(chunks):
        doc_id = f"{source}_{i}"

        collection.add(
            documents=[chunk],
            metadatas=[metadata],
            embeddings=[embeddings[i]],
            ids=[doc_id]
        )

    # ❌ REMOVE THIS - NOT USED IN NEW CHROMA
    # chroma_client.persist()

    return {"status": "stored", "chunks": len(chunks)}


# --------- Retrieve similar content ---------
def retrieve(query):
    q_embed = model.encode([query]).tolist()[0]

    results = collection.query(
        query_embeddings=[q_embed],
        n_results=5
    )
    return results
