## Checkpoint 

### Step 1. ```loader.py``` loads all files

Then it loops:
```
for file in pdf_files:
```
and creates:
```
documents = [
    {
        "filename": "traffic.pdf",
        "text": "Traffic cameras improve road safety..."
    },
    {
        "filename": "safety.pdf",
        "text": "Safety systems reduce accidents..."
    },
    {
        "filename": "cameras.pdf",
        "text": "Camera placement guidelines..."
    }
]
```

So multiple files are already inside the ```documents``` list.


### Step 2. ```chunker.py``` splits all documents


When you pass:

```
chunks = chunk_documents(documents)
```
The chunker loops through every document: ```for document in documents:```

So it processes:
```
traffic.pdf
    ↓
chunk 1
chunk 2
chunk 3


safety.pdf
    ↓
chunk 4
chunk 5


cameras.pdf
    ↓
chunk 6
chunk 7
```

Now the chunks look like:
```
chunks = [
    {
        "filename": "traffic.pdf",
        "text": "Traffic cameras improve road safety..."
    },
    {
        "filename": "traffic.pdf",
        "text": "Cameras detect vehicles..."
    },
    {
        "filename": "safety.pdf",
        "text": "Safety systems reduce accidents..."
    },
    {
        "filename": "cameras.pdf",
        "text": "Camera placement rules..."
    }
]

```
Notice:

One list contains chunks from all files.


### Step 3. Now embeddings

We call: ```embeddings = create_embeddings(chunks)```


Now the function receives:
```
chunks = [
    chunk from traffic.pdf,
    chunk from traffic.pdf,
    chunk from safety.pdf,
    chunk from cameras.pdf
]
```

Inside:
```
for chunk in chunks:
    texts.append(chunk["text"])
```
It extracts:
```
texts = [
    "Traffic cameras improve road safety...",
    "Cameras detect vehicles...",
    "Safety systems reduce accidents...",
    "Camera placement rules..."
]
```
Then:
```
model.encode(texts)
```
creates:
```
[
 vector_for_chunk_1,
 vector_for_chunk_2,
 vector_for_chunk_3,
 vector_for_chunk_4
]
```

The vectors are supposed to be stored or mixed together in the same vector database, even if they came from different files, this is completely fine.

### So the flow is
```
PDF 1 ─┐
PDF 2 ─┼──> loader.py ──> documents list
PDF 3 ─┘

                 ↓

          chunker.py

                 ↓

        chunks from ALL files

                 ↓

          embedder.py

                 ↓

        vector for EACH chunk
```

