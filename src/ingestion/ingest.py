from src.ingestion.loader import load_documents
from src.ingestion.chunker import chunk_documents
from src.ingestion.embeddings import create_embeddings
from src.retrieval.vector_store import store_embeddings


def run_ingestion():

    print("Loading documents...")

    docs = load_documents(
        "src/data"
    )

    print("Documents loaded:", len(docs))


    print("Creating chunks...")

    chunks = chunk_documents(docs)

    print("Chunks created:", len(chunks))


    print("Creating embeddings...")

    embeddings = create_embeddings(chunks)

    print("Embeddings shape:", embeddings.shape)


    print("Storing in ChromaDB...")

    store_embeddings(
        chunks,
        embeddings
    )

    print("Ingestion completed successfully!")


if __name__ == "__main__":
    run_ingestion()