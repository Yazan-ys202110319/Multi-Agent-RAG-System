# It checks whether the answer is acceptable.


def validation_agent(answer, chunks):

    # If no answer has been generated
    if not answer.strip(): # Remove whitespace becacse they are technically not empty
        return {
            "valid": False,
            "answer": "No answer was generated"
        }

    # No retrieved context 
    if len(chunks) == 0:
        return {
            "valid": False,
            "answer": "No relevant documents were found"
        }

    # Else (everything looks fine) 
    else:
        return {
            "valid": True,
            "answer": answer
        }