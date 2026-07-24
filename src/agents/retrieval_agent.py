# This agent job is only retrieve the contexts / chunks from ChromaDB that is related to the user's question


print("a")

from src.retrieval.vector_store import collection
print("b")
from src.ingestion.embeddings import create_query_embedding
print("c")

def retrieval_agent(question):

    # 1- Convert the question to embedding
    query_embedding = create_query_embedding(question)

    # 2- Search ChromaDB for relavent context to the question
    results = collection.query(
        query_embeddings = [query_embedding],
        n_results = 5
    )

    print(results)

    # 3- Extract documents / chunks / context
    chunks = results["documents"][0]


    return chunks

