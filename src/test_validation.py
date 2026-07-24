from src.agents.retrieval_agent import retrieval_agent
from src.agents.reasoning_agent import reasoning_agent
from src.agents.validation_agent import validation_agent


question = "Explain YOLO"

chunks = retrieval_agent(question)

answer = reasoning_agent(question, chunks)

result = validation_agent(answer, chunks)

print(result)