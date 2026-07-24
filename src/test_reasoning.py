from src.agents.retrieval_agent import retrieval_agent
from src.agents.reasoning_agent import reasoning_agent


question = "Explain YOLO"

# Using the retrieval agent get the related chunks to the question 
chunks = retrieval_agent(question)


# Using the resoning agent get the answer from the llm
answer = reasoning_agent(question, chunks)

print(answer)