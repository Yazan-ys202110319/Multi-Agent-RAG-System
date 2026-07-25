


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
    
    Your task is to evaluate whether the generated answer correctly answers the user's question using ONLY the provided context.

    Question:
    {question}

    Context:
    {context}

    Generated Answer: 
    {answer}

    
    Evaluate the answer using the following criteria:

    1. Correctness (40%)
    - Is the information factually correct according to the context?

    2. Completeness (30%)
    - Does the answer cover all important points needed to answer the question?

    3. Grounding (20%)
    - Is every claim supported by the provided context?
    - Do not reward information that is not found in the context.

    4. Clarity (10%)
    - Is the answer well-written, easy to understand, and logically organized?

    Scoring:
    - 1-3: Poor
    - 4-5: Fair
    - 6-7: Good
    - 8-9: Very Good
    - 10: Excellent

    Be strict.
    Only give a score of 10 if the answer is completely correct, comprehensive, fully supported by the context, and clearly written.
    If any important information is missing, the score should be 9 or lower.

    Determine whether the answer is VALID or INVALID.
    An answer is VALID if it is factually correct and sufficiently answers the user's question using the provided context.

    Return EXACTLY in this format:

    SCORE: <1-10>
    STATUS: <VALID or INVALID>
    REASON: <one short sentence>

    Do not include any additional text.

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
    
