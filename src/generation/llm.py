


import requests



def generate_answer(question, context):
    # question --> the user question 
    # context → the text / documents retrieved from ChromaDB


    # Create the prompt 
    prompt = f"""
    You are a helpful AI research assistant.
    
    Use ONLY the information provided in the context below.

    If the answer cannot be found in the context, reply:
    "I don't have enough information in the provided documents."

    Context:
    {context}

    Question:
    {question}

    Answer:
    """

    # Sending the request to Ollama
    response = requests.post(
        # This is Ollama's API running on your own computer.
        # So we are talking directly to the local Mistral model.
        "http://localhost:11434/api/generate",
        # Sending information
        json = {
            "model": "mistral",
            "prompt": prompt,
            "stream": False # means ollama wait until the full answer is finished, then send it back.
        }

    )

    # Ollama returns JSON file that has the model name, reponse (the answer of the prompt), done status.
    # Now we want to extract the answer from the response JSON file from Ollama.
    return response.json()["response"]


