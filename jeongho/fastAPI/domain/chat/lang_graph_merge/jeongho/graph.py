from langgraph.graph import StateGraph, START, END
from domain.chat.lang_graph_merge.jeongho.state import subOverallState, InputState, OutputState
from domain.chat.lang_graph_merge.state import OverallState
from domain.chat.lang_graph_merge.jeongho.queryDecompose import queryDecompose
from domain.chat.lang_graph_merge.jeongho.multiQueryExpansion import multiQueryExpansion
from domain.chat.lang_graph_merge.jeongho.multiQueryExpansion import multiQueryExpansion
from domain.chat.lang_graph_merge.jeongho.hybridCC import hybridCC
from domain.chat.lang_graph_merge.jeongho.cohereRerank import cohereRerank
from domain.chat.lang_graph_merge.jeongho.generate import generateAnswer
from domain.chat.lang_graph_merge.jeongho.merge import merge


builder = StateGraph(subOverallState, input=InputState, output=OverallState)

builder.add_node("queryDecompose", queryDecompose)
builder.add_node("multiQueryExpansion", multiQueryExpansion)
builder.add_node("hybridCC", hybridCC)
builder.add_node("cohereRerank", cohereRerank)
builder.add_node("generateAnswer", generateAnswer)
builder.add_node("merge", merge)

builder.add_edge(START, "queryDecompose")
builder.add_edge("queryDecompose", "multiQueryExpansion")
builder.add_edge("multiQueryExpansion", "hybridCC")
builder.add_edge("hybridCC", "cohereRerank")
builder.add_edge("cohereRerank", "generateAnswer")
builder.add_edge("generateAnswer", "merge")
builder.add_edge("merge", END)

subgraph = builder.compile()