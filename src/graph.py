# This file will decides which agent runs next and the graph.


from typing import TypedDict

from langgraph.graph import StateGraph, START, END


from src.agents.retrieval_agent import retrieval_agent
from src.agents.reasoning_agent import reasoning_agent
from src.agents.validation_agent import validation_agent


# Step 1- Creating the state

class AgentState(TypedDict):

    question: str
    chunks: str
    answer: str
    valid: bool
    retries: int
    feedback: str # "Why is it invalid and how should the reasoning agent improve it?"
    score: int


# Step 2- Creating the nodes for each agent

# Retrieval node
def retrieval_node(state: AgentState):

    # Get the question from the state
    chunks = retrieval_agent(state["question"])

    # Now call the retrieval agent to get the related chunks to the question and store it in the (chunk) states
    
    state["chunks"] = chunks

    return state

# question
#    |
#    ↓
# retrieval_agent()
#    |
#    ↓
# chunks



# Reasoning node

def reasoning_node(state: AgentState):

    print("\n--- REASONING ---")
    print("Feedback:", state["feedback"])

    answer = reasoning_agent(state["question"], state["chunks"], state["feedback"])

    print("Answer:", answer)

    state["answer"] = answer

    

    return state

# question + chunks
#         |
#         ↓
#  reasoning_agent()
#         |
#         ↓
#      answer

# Validation node
def validation_node(state: AgentState):

    print("\n--- VALIDATION ---")

    results = validation_agent(state["question"], state["answer"], state["chunks"])

    print("Score:", results["score"])
    print("Valid:", results["valid"])
    print("Feedback:", results["feedback"])

    # Get the final answer and validation from the agent, the answer might change in case the valid = False (check the agent code)

    # If valid = True, the answer will be as it is coming from reasoning_node (so without chaning) 
    state["answer"] = results["answer"]
    state["valid"] = results["valid"]
    state["feedback"] = results["feedback"]
    state["score"] = results["score"]


    state["retries"] += 1 # add one more retry

    return state


# answer + chunks
#        |
#        ↓
# validation_agent()
#        |
#        ↓
# valid / invalid


# the routing function, it decide where to go next.
def check_validation(state: AgentState):

    print("\n--- ROUTING ---")

    if state["valid"] == True:
        return "end"

    if state["retries"] >= 3:
        return "end"

    # otherwise (lesss than 3 and not true)
    return "retry" # Try improving answer



# Step 3- Build the graph

graph_builder = StateGraph(AgentState)


# Add the nodes 

graph_builder.add_node(
    "retrieval", # the name of the agent
    retrieval_node # the method for this agent / node
)

graph_builder.add_node(
    "reasoning", 
    reasoning_node
)

graph_builder.add_node(
    "validation",
    validation_node
)


# Step 4- Connect the agent

graph_builder.add_edge(
    START,
    "retrieval"
)

graph_builder.add_edge(
    "retrieval",
    "reasoning"
)

graph_builder.add_edge(
    "reasoning",
    "validation"
)


# Make the validation agent retry if the validation is wrong, so the graph now can choose paths
graph_builder.add_conditional_edges(
    "validation",
    check_validation,
    { # in langGraph it is a special routing dictionary that tells the graph where to go based on the result of a decision function.
        "end": END,
        "retry": "reasoning"
    }
)



# Step 5- Compile the graph

graph = graph_builder.compile() # Now graph has the workflow





