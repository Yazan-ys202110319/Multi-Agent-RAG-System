# Now we have the vectors stored in memory: in the embeddings variable.
# but when you close your notebook, the vectors will disappear.


# A vector database will:

# store the embeddings
# store the original text
# search for similar chunks later

print("First")
import chromadb
print("second")
from pathlib import Path # to build the path for the chroma 

BASE_DIR = Path(__file__).resolve().parents[2]
# __file__ means: the current file location 
# .resolve() gets the absolute / full path of the file
# parents goes to the parent folder of the current file
DB_PATH = BASE_DIR / "chroma_db" # chroma db path

print("Using ChromaDB at:", DB_PATH)

client = chromadb.PersistentClient(path=str(DB_PATH))


collection = client.get_or_create_collection(name="research_papers") # If name exists retrieves and returns the existing collection.

print("third")

# This method is responsible for storing the chunks and their embeddings / vectors in ChromaDB.
def store_embeddings(chunks, embeddings):

    ids = [] # This will store the ids 
    documents = [] # This will store the documents 


    # This loop will go or iterate over 2 things: i --> which will represent one chunk or an index.
    # chunk --> will have the actual chunk text and ignore the file name.
    # enumerate() gives you both the index and the chunk. 
    for i, chunk in enumerate(chunks):
        # ChromaDB requires every document to have a unique ID, and they must be string.
        ids.append(str(i))
        documents.append(chunk["text"]) # Get the text from chunk and append it 


    # Add everything to ChromaDB
    # We are telling ChromaDB for chunks store the document (the chunk) with its embeddings / vector.
    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings.tolist(), # In embeddings.py when we do (model.encode(text)) it will return a NumPy array.
        # But ChromaDB expects a regular Python list.
        metadatas=[
            {"filename": chunk["filename"]} # Store the filename from the chunk for the metadata
            for chunk in chunks # For each chunk in chunks
        ]
    )


    return collection



# Next step is about retrieval (searching your documents to answer a query from the user)

# This function is responsible for searching your ChromaDB vector database 
# and retrieving the most relevant document chunks for a user's query.
def search_documents(query_embedding, n_results = 3):
    # query_embedding --> This is the vector representation of the user's question.
    # For all-MiniLM-L6-v2, this vector has 384 dimensions:

    # n_results = 3 --> This controls how many matching documents you want back (the closest).

    results = collection.query(
        query_embeddings = [query_embedding.tolist()], # In case the user query was a NumPy array convert it to list
        # after it will be like: [[0.12, 0.98, 0.84]]
        n_results = n_results
    )

    # To get the texts and the metadats from ChromDB
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    
    return documents, metadatas


