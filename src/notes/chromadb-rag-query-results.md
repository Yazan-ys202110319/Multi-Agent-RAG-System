# Understanding ChromaDB Query Results in a RAG System

## Overview

In a Retrieval-Augmented Generation (RAG) system, ChromaDB is responsible for storing documents and finding the most relevant pieces of information when a user asks a question.

A common point of confusion is:

> "Where did the `results` dictionary come from?"

The answer:

**You did not create it. ChromaDB automatically creates and returns it when you call `collection.query()`.**

This document explains the complete flow:

1. Storing documents in ChromaDB
2. Creating query embeddings
3. Searching the vector database
4. Understanding the returned `results` dictionary
5. Extracting documents and metadata
6. Passing retrieved context to the LLM

---

## 1. Storing Data in ChromaDB

Before searching, we first need to add documents into ChromaDB.

```python
collection.add(
    ids=ids,
    documents=documents,
    embeddings=embeddings.tolist(),
    metadatas=[
        {"filename": chunk["filename"]}
        for chunk in chunks
    ]
)
```

This stores four important things:

- ID
- Document text
- Embedding vector
- Metadata

### Example Document

Imagine we have a PDF called `transformers.pdf`. Inside this PDF we have a chunk:

```python
chunk = {
    "filename": "transformers.pdf",
    "text": "Transformers use attention mechanisms."
}
```

The embedding model converts the text into a vector:

```python
embedding = [0.23, 0.55, -0.12, ...]
```

Now ChromaDB stores them together.

### What ChromaDB Stores

```
                ChromaDB
                    |
        -----------------------------
        |             |             |
        ↓             ↓             ↓
      Text        Vector       Metadata

"Transformers     [0.23,      {
 use attention     0.55,       "filename":
 mechanisms."     -0.12]       "transformers.pdf"
                               }
```

So each item in ChromaDB contains:

```
ID
 ├── Document Text
 ├── Embedding Vector
 └── Metadata
```

---

## 2. User Asks a Question

Now a user asks:

> "Explain transformers in simple words"

This question is just text. However, ChromaDB cannot compare text directly — it compares vectors. Therefore, we convert the question into an embedding.

### Creating the Question Embedding

```
User Question
"Explain transformers in simple words"
          |
          ↓
   Embedding Model
          |
          ↓
   Question Vector
[0.44, 0.21, -0.11, ...]
```

Now both stored documents and the user question are represented as vectors.

---

## 3. Searching ChromaDB

We send the question vector to ChromaDB:

```python
results = collection.query(
    query_embeddings=[question_embedding.tolist()],
    n_results=3
)
```

This means: *"Find the 3 stored vectors that are closest in meaning to my question vector."*

---

## 4. How ChromaDB Finds Similar Documents

Imagine ChromaDB contains these documents:

**Document 1**
- ID: `0`
- Text: `"Transformers use attention mechanisms."`
- Vector: `[0.23, 0.55, -0.12]`
- Metadata: `{"filename": "transformers.pdf"}`

**Document 2**
- ID: `1`
- Text: `"Neural networks contain layers."`
- Vector: `[0.11, 0.88, 0.33]`
- Metadata: `{"filename": "deep_learning.pdf"}`

The question vector `[0.44, 0.21, -0.11]` is compared against all stored vectors:

```
             Question Vector
                    |
                    ↓
             Compare similarity
                    |
     --------------------------------
     Document 1 Vector
     Document 2 Vector
     Document 3 Vector
     Document 4 Vector
```

ChromaDB selects the closest matches.

---

## 5. ChromaDB Returns the Results Dictionary

After searching, ChromaDB creates a dictionary:

```python
results = {
    "ids": [["0", "5", "8"]],

    "documents": [[
        "Transformers use attention mechanisms.",
        "Attention helps models understand relationships.",
        "Transformers process sequences."
    ]],

    "metadatas": [[
        {"filename": "transformers.pdf"},
        {"filename": "attention.pdf"},
        {"filename": "nlp.pdf"}
    ]],

    "distances": [[0.12, 0.18, 0.21]]
}
```

---

## 6. Understanding the Results Dictionary

### IDs

```python
results["ids"]
# [["0", "5", "8"]]
```

These are the identifiers of the retrieved chunks.

### Documents

```python
results["documents"]
# [[
#   "Transformers use attention mechanisms.",
#   "Attention helps models understand relationships.",
#   "Transformers process sequences."
# ]]
```

These are the actual text chunks retrieved from your documents.

### Metadata

```python
results["metadatas"]
# [[
#   {"filename": "transformers.pdf"},
#   {"filename": "attention.pdf"}
# ]]
```

Metadata tells you where each chunk came from — for example, that a given answer came from `transformers.pdf`.

### Distances

```python
results["distances"]
# [[0.12, 0.18, 0.21]]
```

These represent how close each document is to the question. Usually, **smaller distance = more similar**.

---

## 7. Why Does ChromaDB Return a Dictionary?

ChromaDB *could* return just a flat list of text:

```python
["Transformers use attention mechanisms.", "Attention helps models"]
```

But then you'd lose important information:

- Where did this come from?
- What was the ID?
- How similar was it?

Therefore, ChromaDB returns a dictionary containing `documents`, `metadatas`, `ids`, and `distances` together.

---

## 8. Why Do We Use `[0]`?

This is one of the most confusing parts.

ChromaDB supports multiple questions at the same time, e.g.:

```python
[question1_embedding, question2_embedding, question3_embedding]
```

It would return results for question 1, question 2, and question 3 — grouped by query.

For example, `results["documents"]` gives:

```python
[
    ["chunk 1", "chunk 2", "chunk 3"]
]
```

The **first list** represents the query. The **second list** contains the retrieved documents for that query.

So `results["documents"][0]` means: *"Give me the documents retrieved for the first question."*

Output:

```python
["chunk 1", "chunk 2", "chunk 3"]
```

---

## 9. Complete RAG Flow

```
                User
                 |
                 ↓
      "Explain transformers"
                 |
                 ↓
        Embedding Model
                 |
                 ↓
        Question Vector
                 |
                 ↓
            ChromaDB
                 |
                 ↓
      Similarity Search
                 |
                 ↓
          Results Dictionary
                 |
     -------------------------
     documents / metadata / ids / distances
     -------------------------
                 |
                 ↓
          Extract Documents
       results["documents"][0]
                 |
                 ↓
              Context
                 |
                 ↓
             Mistral LLM
                 |
                 ↓
              Final Answer
```

---

## 10. Preparing Context for the LLM

Usually we only need the text:

```python
context = "\n".join(results["documents"][0])
```

**Before:**

```python
[
    "Transformers use attention mechanisms.",
    "Attention helps models understand relationships.",
    "Transformers process sequences."
]
```

**After:**

```
Transformers use attention mechanisms.
Attention helps models understand relationships.
Transformers process sequences.
```

---

## 11. Sending Information to Mistral

Now we send:

**Question:** "Explain transformers in simple words."

**Retrieved Context:**
```
Transformers use attention mechanisms.
Attention helps models understand relationships.
Transformers process sequences.
```

```
        |
        ↓
      Mistral LLM
        |
        ↓
   Generated Answer
```

---

## Key Idea to Remember

ChromaDB stores:

**Document + Embedding Vector + Metadata**

When searching:

```
Question → Embedding Model → Question Vector → ChromaDB Search → Results Dictionary
```

The results dictionary contains:

```
results
 |---- documents
 |---- metadatas
 |---- ids
 |---- distances
```

Your code:

```python
results = search_documents(question_embedding)
```

creates:

```
results
 ├── documents   → Retrieved text chunks
 ├── metadatas   → Source filenames
 ├── ids
 └── distances
```

> **The most important concept:** ChromaDB does not generate answers. It only finds the most relevant pieces of information. The LLM (Mistral) uses those retrieved documents to generate the final answer.
