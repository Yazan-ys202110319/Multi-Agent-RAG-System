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
    valid: str


# Step 2- Creating the nodes for each agent

# Retrieval node
def retrieval_agent(state: AgentState):

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

    answer = reasoning_agent(state["question"], state["chunks"])

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

    results = validation_agent(state["answer"], state["chunks"])

    # Get the final answer and validation from the agent, the answer might change in case the valid = False (check the agent code)

    # If valid = True, the answer will be as it is coming from reasoning_node (so without chaning) 
    state["answer"] = results["answer"]
    state["valid"] = results["valid"]


    return state


# answer + chunks
#        |
#        ↓
# validation_agent()
#        |
#        ↓
# valid / invalid



# Step 3- Build the graph

graph_builder = StateGraph(AgentState)


# Add the nodes 

graph_builder.add_node(
    "retrieval", # the name of the agent
    retrieval_agent # defining the method for this agent
)

graph_builder.add_node(
    "reasoning", 
    reasoning_agent
)

graph_builder.add_node(
    "validation",
    validation_agent
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


graph_builder.add_edge(
    "validation",
    END
)



