# Now we have the vectors stored in memory: in the embeddings variable.
# but when you close your notebook, the vectors will disappear.


# A vector database will:

# store the embeddings
# store the original text
# search for similar chunks later


import chromadb


# =============================================================


# Lesson 2

# Why the data disappers when using the regular client? You can fix it using Persistent Client. 
# How to make the data available across and can be used in mutltiple scripts.



# chromadb.client() --> stores data in the memory --> Data is lost
# chromadb.persistentclient() --> stores data on disk (folder) --> Data is saved


client = chromadb.PersistentClient(path='./chroma_db') # path where you want to save

collection = client.get_or_create_collection(name="research_papers") # If name exists retrieves and returns the existing collection.


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
        embeddings=embeddings.tolist() # In embeddings.py when we do (model.encode(text)) it will return a NumPy array.
        # But ChromaDB expects a regular Python list.
    )

    print(collection)

    return collection


