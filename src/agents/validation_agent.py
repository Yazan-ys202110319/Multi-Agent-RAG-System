# It checks whether the answer is acceptable.

import re

from src.generation.llm import vaalidate_answer

def validation_agent(question, answer, chunks):

    
    context = "\n".join(chunks)

    result = vaalidate_answer(
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


    return {
        "valid": valid,
        "answer": answer,
        "feedback": result,
        "score": score
    }


    