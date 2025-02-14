from langgraph.graph import StateGraph, START, END
from domain.chat.lang_graph_merge.state import OverallState
from domain.chat.lang_graph_merge.hyeseo.temp_node1 import temp_node1
from domain.chat.lang_graph_merge.hyeseo.temp_node2 import temp_node2
from domain.chat.lang_graph_merge.hyeseo.temp_node3 import temp_node3


builder = StateGraph(OverallState, input=OverallState, output=OverallState)

builder.add_node("temp_node1", temp_node1)
builder.add_node("temp_node2", temp_node2)
builder.add_node("temp_node3", temp_node3)

builder.add_edge(START, "temp_node1")
builder.add_edge("temp_node1", "temp_node2")
builder.add_edge("temp_node2", "temp_node3")
builder.add_edge("temp_node3", END)

sony_subgraph = builder.compile()