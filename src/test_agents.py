print("0")

from src.agents.retrieval_agent import retrieval_agent

print("1")

question = "Explain YOLO"

print("2")

chunks = retrieval_agent(question)

print("3")

for chunk in chunks:
    print(chunk)