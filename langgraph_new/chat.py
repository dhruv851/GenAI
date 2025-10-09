from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(model="gpt-4o")
                      
class State(TypedDict):
    messages: Annotated[list, add_messages]

def chatboot(state: State):
    response = llm.invoke(state.get("messages")) 

    return {"messages":[response]}

def samplenode(state: State):
    print("\n\nInside sample node",state)
    return {"messages":["Sample Message Appended"]}

graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatboot)
graph_builder.add_node("samplenode", samplenode)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "samplenode")
graph_builder.add_edge("samplenode", END)

graph = graph_builder.compile()

updated_state=graph.invoke(State({"messages":["Hey My name is dhruv sonani"]}))
print("\n\nUpdated State:",updated_state)

# START -> chatBot ->samplenode -> END

# state = { message :  ["Hey there"]}
# node runs : chtBot(state:["Hey there"]) -> ["Hi, This is a message from ChatBot."]
# state = { "messages" : ["Hey there", "Hi, This is a message from ChatBot."]}
