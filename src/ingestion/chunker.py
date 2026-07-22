# Because we can not send the entire text to the LLM or the embedding model we need to chunck it first into small text pieces

def chunk_documents(documents, chunk_size = 500): # will receive the output of load_documents()
    # chunk_size --> the maximum amount of text that each chunk will contain.

    # Store the final chunks 
    chunks = []

    for document in documents: # for each document

        text = document["text"] # Get the text from the document


# Split the text, it will go from 0 up to the whole document size (len(text)) and split it with chunk size
        for i in range(0, len(text), chunk_size): 

            # Create each chunk of the document. the format is text[start : end]
            chunk = text[i:i + chunk_size] # i here to move the pointer because chunk_size is fixed

            # Store the chunk, in chunks and get the document name for "filename" and store the chunk under "text"
            chunks.append({
                "filename": document["filename"],
                "text": chunk
            })

    return chunks

# Later each chunk will become a vector 
