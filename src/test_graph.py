from src.graph import graph


# compile() creates the workflow but it does not excute anything so you need to use invoke(initial_state) to actually run the agents
result = graph.invoke(
    {
        "question": "Explain YOLO",
        "chunks": [],
        "answer": "",
        "valid": False
    }
)


print(result)