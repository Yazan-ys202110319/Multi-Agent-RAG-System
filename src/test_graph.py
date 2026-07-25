from src.graph import graph


result = graph.invoke(
    {
        "question": "What is YOLO?",
        "chunks": [],
        "answer": "",
        "valid": False,
        "feedback": "",
        "retries": 0,
        "score": 0
    }
)


print(result)