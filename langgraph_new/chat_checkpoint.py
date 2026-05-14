from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.mongodb import MongoDBSaver

load_dotenv()

llm = ChatOpenAI(model="gpt-4o")
                      
class State(TypedDict):
    messages: Annotated[list, add_messages]

def chatboot(state: State):
    response = llm.invoke(state.get("messages")) 

    return {"messages":[response]}

graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatboot)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()

def compile_graph_with_checkpointer(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)

DB_URI = "mongodb://admin:admin@localhost:27017/"
with MongoDBSaver.from_conn_string(DB_URI) as checkpointer:
    graph_with_checkpointer = compile_graph_with_checkpointer(checkpointer=checkpointer)

    config = {
        "configurable":{
            "thread_id":"dhruv" #user-id
        }
    }
    for check in graph_with_checkpointer.stream(
        State({"messages":["What i am learning"]}),

        config,
        stream_mode="values"
):
        check["messages"][-1].pretty_print()


# START -> chatBot ->samplenode -> END

# state = { message :  ["Hey there"]}
# node runs : chtBot(state:["Hey there"]) -> ["Hi, This is a message from ChatBot."]

# Checkpointing(dhruv) = Hey My name is Dhruv Sonani
