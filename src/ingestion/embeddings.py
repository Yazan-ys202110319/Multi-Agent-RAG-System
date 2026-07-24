# Convert each text chunk into a numerical vector that a LLM can compare.
# Before: "Traffic cameras improve road safety" after embeddings: [0.352, -0.2524, 0.6955]


from sentence_transformers import SentenceTransformer # This library provides pretrained models that convert text into vectors


model = None

def get_model(): # Lazy load the embedding model

    global model

    if model is None:
        model = SentenceTransformer("all-MiniLM-L6-v2")
        print("Embedding model loaded")

    return model


def create_embeddings(chunks): # Receives a list of chunks from all documents
    # chunks will have chunks from all files 

    model = get_model()

    # Extract the text from each chunk of the file
    texts = []

    for chunk in chunks:

        texts.append(chunk["text"])

    embeddings = model.encode(texts) # covert to vectors, each chunk will get 1 vector 

    return embeddings


# This function to convert a question to a vector not chunks as the above 
def create_query_embedding(question):


    model = get_model()

    embedding = model.encode(question)

    return embedding
