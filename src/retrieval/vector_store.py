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



