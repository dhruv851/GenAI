from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Annotated, Optional, Literal
from langgraph.graph import StateGraph, START, END
from openai import OpenAI

load_dotenv()

client = OpenAI()

class State(TypedDict):
    user_query: str
    llm_output: Optional[str]
    is_good: Optional[bool]

def chatBot(state: State):
    print("\n\nInside chatBot node",state)
    response = client.chat.completions.create(
        model="gpt-4o",  
        messages=[
            {"role": "user", "content": state.get("user_query")}
        ]
    )
    state["llm_output"] = response.choices[0].message.content
    return state

def evaluate_response(state: State) -> Literal["chatbot_gemini", "endnode"]:
    print("\n\nInside evaluate_response node",state)
    if True:
        return "endnode"
    return "chatbot_gemini"

def chatbot_gemini(state: State):
    print("\n\nInside chatBot_gemini node",state)
    response = client.chat.completions.create(
        model="gpt-5",  
        messages=[
            {"role": "user", "content": state.get("user_query")}
        ]
    )
    state["llm_output"] = response.choices[0].message.content
    return state

def endnode(state: State):
    print("\n\nInside endnode",state)
    return state

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatBot)
graph_builder.add_node("chatbot_gemini", chatbot_gemini)
graph_builder.add_node("endnode", endnode)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", evaluate_response)

graph_builder.add_edge("chatbot_gemini", "endnode")
graph_builder.add_edge("endnode", END)

graph = graph_builder.compile()
updated_state = graph.invoke(State({"user_query":"Hi, What is 2 + 2 ?"}))
print("\n\nUpdated State:", updated_state)