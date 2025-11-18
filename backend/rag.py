from embeddings import retrieve


def rag_query(query):
    """
    Retrieves relevant chunks and creates a final context block.
    """
    results = retrieve(query)

    context = ""
    for doc in results["documents"][0]:
        context += doc + "\n\n"

    return context
