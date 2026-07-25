


import requests



def generate_answer(question, context, feedback):
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

    Previous answer feedback:
    {feedback}

    Generate an improved answer.
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


# Check the answer by the llm
def vaalidate_answer(question, answer, context):

    prompt = f"""
    You are an answer quality evaluator.
    Your job is to check if the generated answer correctly answers the question
    using ONLY the provided context.

    Question:
    {question}

    Context:
    {context}

    Generated Answer: 
    {answer}

    Check:
    1. Is the answer relevant to the question?
    2. Is the answer supported by the context?
    3. Does the answer contain incorrect information?

    
    Evaluate the answer quality.
    
    Give a score from 1 to 10.

    1 = completely wrong
    10 = excellent answer

    You MUST follow this exact format:

    SCORE: 1-10

    STATUS: VALID or INVALID

    REASON:
    one sentence explanation


    Do not add anything else.

    """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json = {
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )


    return response.json()["response"]
    
