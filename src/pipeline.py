# This is the manager that will connect all components


from src.ingestion.embeddings import create_query_embedding
from src.retrieval.vector_store import search_documents
from src.generation.llm import generate_answer


def ask_question(question):


    # 1. Convert question to vector so we can search with the vector for similar text in chromaDB
    query_embedding = create_query_embedding(question)

    # 2. Search ChromaDB for related text to the question
    results = search_documents(query_embedding)

    # 3. Get the context that is related to the user question to later give it to the llm for better answer
    context = "\n".join(
        results["documents"][0]
    )

    # 4. Ask the LLM
    answer = generate_answer(
        context = context,
        question = question
    )

    return answer


print(ask_question("Explain YOLO"))
