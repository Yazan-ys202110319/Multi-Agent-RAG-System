# This is the resoning agent, it will take the user's question + retrieved chunks → use the LLM → generate an answer.

from src.generation.llm import generate_answer

def reasoning_agent(question, chunks):

    # Convrt retrieved chunks into one context string
    context = "\n".join(chunks)

    # Ask the LLM
    answer = generate_answer(question = question, context = context)

    return answer


