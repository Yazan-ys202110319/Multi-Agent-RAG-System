from fastapi import FastAPI
from pydantic import BaseModel
# FastAPI uses Pydantic to:
# validate incoming data
# make sure the input has the correct format and handles wrong inputs


# Import the RAG pipline 
from src.pipeline import ask_question


app = FastAPI(title = "Multi-Agent RAG System") # Create the API application, and give it a name


# Creating a Pydantic model
class QuestionRequest(BaseModel):
    question : str # The user question must be of type string
    # Every request sent to /ask must contain a field called question and it must be a string.

# post because the user is sending data in /ask page
@app.post("/ask") # When someone sends a POST request to /ask, run the function below.
def ask(request : QuestionRequest): 
    # request --> is the data / question sent be the user
    # Now FastAPI will convert the incoming JSON from the user (request) into a QuestionRequest object to validate.


    # Example: Incoming: 
    # {
    #     "question":"What is RAG?"
    # }

    # It will become: request.question --> to get the value of what the user sent. so the value will be: "What is RAG"



    # Here is where the API connects to the AI / RAG system.
    answer = ask_question(request.question) 

    # Returning the response from my RAG system
    # We return a dictionary and FastAPI will converts it to JSON
    return {
        "answer": answer
    }


#                 User
#                   |
#                   |
#                   v
#               POST / ask
#                   |
#                   v
#                 api.py
#             (FastAPI layer)
#                   |
#                   v
#              pipeline.py
#            (RAG controller)
#                   |
#                   v
#       ---------------------
#       |          |        |
#  ChromaDB   Embedding    LLM