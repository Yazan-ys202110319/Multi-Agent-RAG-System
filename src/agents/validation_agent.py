# It checks whether the answer is acceptable.

import re

from src.generation.llm import validate_answer

def validation_agent(question, answer, chunks):

    
    context = "\n".join(chunks)

    result = validate_answer(
        question, 
        answer,
        context
    )

    if "STATUS: VALID" in result.upper():
        valid = True
    else:
        valid = False


    print("Validator response:")
    print(result)


    score_match = re.search(r"SCORE:\s*(\d+)", result)


    if score_match:
        score = int(score_match.group(1))
    else:
        score = 0


        # Extract feedback/reason
    feedback_match = re.search(
        r"REASON:\s*(.*)",
        result
    )

    if feedback_match:
        feedback = feedback_match.group(1)
    else:
        feedback = "No feedback provided"

    return {
        "valid": valid,
        "answer": answer,
        "feedback": feedback,
        "score": score
    }


    