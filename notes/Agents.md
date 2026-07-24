#### At first there is almost no intelligence in the retrieval agent. For now, we are building the skeleton first. After the three agents exist, we add the decision-making layer.

- The "agent" part comes from:

  - deciding what to do,
  - choosing tools,
  - evaluating results,
  - changing its plan.

LangGraph helps you build that decision flow.

---

### Retrieval Agent
- Its job is to search for the relevant documents / chunks / contexts from ChromaDB that are realted to the user's question.

```
Question
   |
   ↓
Retrieval Agent
   |
   ↓
Relevant Chunks
```

---

### Reasoning Agent
Its job is to take the user's question + retrieved chunks → use the LLM → generate an answer.


The architecture now becomes:

```
User Question
      |
      ↓
Retrieval Agent ✅
      |
      ↓
Relevant Chunks
      |
      ↓
Reasoning Agent ⬅️ (we build this now)
      |
      ↓
Draft Answer
```

---

### Validation agent

#### What should a validation agent do? 

A validation agent doesn't generate a new answer.

It checks whether the answer is acceptable.

