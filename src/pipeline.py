# This is the manager that will connect all components


from src.ingestion.embeddings import create_query_embedding

from src.retrieval.vector_store import search_documents

from src.generation.llm import generate_answer


def ask_question(question):


    # 1. Convert question to vector so we can search with the vector for similar text in chromaDB
    query_embedding = create_query_embedding(question)

    # 2. Search ChromaDB for related texts and there metadatas to the user question
    documents, metadatas = search_documents(query_embedding)
    # So we will get the context that is related to the user question to later give it to the llm for better answer
    # decuments will have the related context to the user question and metadatas will have the sources of each chunk / context

    
    # 3. Convert the list of chunks into a one context string that is related to the user question
    context = "\n".join(documents)


    # 4. Generate answer usign the LLM
    answer = generate_answer(
        context = context,
        question = question
    )


    # 5. Get the sources 
    source = set()

    for metadata in metadatas:

        if metadata: # if metadata exists
            source.add(metadata["filename"]) # Get the name of the source


    return {
        "answer": answer, # answer has the texts / chunks / context that are related to the user question and later will be send to the LLM
        "sources": list(source) # Convert back to a list
    }


