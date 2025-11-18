from sentence_transformers import SentenceTransformer
import chromadb

model = SentenceTransformer("all-MiniLM-L6-v2")

chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection("knowledge_base")


# Simple text splitter (no langchain needed)
def simple_splitter(text, chunk_size=400, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

def embed_and_store(text, metadata):
    chunks = simple_splitter(text)

    embeddings = model.encode(chunks).tolist()

    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            metadatas=[metadata],
            embeddings=[embeddings[i]],
            ids=[f"{metadata['source']}_{i}"]
        )

def retrieve(query):
    q_embed = model.encode([query]).tolist()[0]
    results = collection.query(query_embeddings=[q_embed], n_results=5)
    return results
