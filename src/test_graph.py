from src.graph import graph


result = graph.invoke(
    {
        "question": "What is YOLO?",
        "chunks": [],
        "answer": "",
        "valid": False,
        "feedback": "",
        "score": 0,
        "retries": 0
    }
)


print("\n========== FINAL RESULT ==========")

print(result)


