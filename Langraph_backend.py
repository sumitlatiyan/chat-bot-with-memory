#StateGraph is the main LangGraph class to define a workflow as a graph of nodes.
from langgraph.graph import StateGraph, START, END
#Annotated lets you attach metadata to types
from typing import TypedDict, Annotated
#HumanMessage, AIMessage, SystemMessage
from langchain_core.messages import BaseMessage
#A checkpointer that stores graph execution state in RAM (not on disk).
from langgraph.checkpoint.memory import InMemorySaver
#when your node returns {"messages": [new_message]}, LangGraph will append it to the existing messages list rather than overwrite it.
from langgraph.graph.message import add_messages
from Constants import GROQ_API_KEY
from langchain_groq import ChatGroq
import os
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

# Model
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.0,
    max_retries=2,
)
"""messages is a list of BaseMessage objects.
The Annotated[..., add_messages] part tells LangGraph:

when multiple updates to messages occur, combine them by appending messages (using add_messages) instead of replacing the list."""
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):
    messages = state['messages']
    response = llm.invoke(messages)
    return {"messages": [response]}

# Checkpointer This is how LangGraph can persist the state between invocations
checkpointer = InMemorySaver()

graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)
#Providing checkpointer=... enables storing state checkpoints.
chatbot = graph.compile(checkpointer=checkpointer)
