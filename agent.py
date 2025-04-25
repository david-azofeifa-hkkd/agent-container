import os, getpass
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition, ToolNode
from IPython.display import Image, display
from fetch_confluence import ConfluenceFetch
import json
from dotenv import load_dotenv
from openai import AzureOpenAI
import os

load_dotenv()
deployment_name = os.environ['COMPLETIONS_MODEL']

api_key = ("OPENAI_API_KEY")

azure_endpoint = os.environ['AZURE_OPENAI_ENDPOINT']

api_version = os.environ['OPENAI_API_VERSION']

confluence_key = os.environ["CONFLUENCE_API_KEY"]
confluence_user = os.environ["CONFLUENCE_USERNAME"]

# openai_api_key = os.environ['OPENAI_API_KEY']
azure_gpt40 = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=azure_endpoint,
    api_key=api_key
)


def search_confluence(title: str, limit: int = None) -> json:
    '''
    Return found json given a title

    Args:
        title: Substring that can appear in titles of entries
        limit: limit the amount of entries received
    '''
    title = "title ~ " + title
    cf = ConfluenceFetch(key=confluence_key, usr=confluence_user)
    return cf.general_search(search=title, limit=limit)

tools = [search_confluence]
llm = ChatOpenAI(model="gpt-4o")
llm_with_tools = llm.bind_tools(tools)

# System message
sys_msg = SystemMessage(content="You are a helpful assistant tasked with finding wiki entries called pages within confluence based on given title.")

# Node
def assistant(state: MessagesState):
   return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}

# Graph
builder = StateGraph(MessagesState)

# Define nodes: these do the work
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

# Define edges: these determine how the control flow moves
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
    # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
    tools_condition,
)
builder.add_edge("tools", "assistant")
react_graph = builder.compile()

messages = [HumanMessage(content="Find entries that have titles with the word 'data'")]
messages = react_graph.invoke({"messages": messages})
for m in messages['messages']:
    m.pretty_print()