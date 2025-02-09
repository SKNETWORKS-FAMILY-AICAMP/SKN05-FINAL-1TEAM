from langgraph.graph import StateGraph, START, END
from state import OverallState, InputState, OutputState, RetrievalState
from queryDecompose import queryDecompose
from multiQueryExpansion import multiQueryExpansion
from hybridCC import hybridCC
from cohereRerank import cohereRerank
from generate import generateAnswer
from merge import merge

# builder = StateGraph(OverallState, input=InputState, output=OutputState)
builder = StateGraph(OverallState, input=InputState)

builder.add_node(queryDecompose, "queryDecompose")
builder.add_node(multiQueryExpansion, "multiQueryExpansion")
builder.add_node(hybridCC, "hybridCC")
builder.add_node(cohereRerank, "cohereRerank")
builder.add_node(generateAnswer, "generateAnswer")
builder.add_node(merge, "merge")

builder.add_edge(START, "queryDecompose")
builder.add_edge("queryDecompose", "multiQueryExpansion")
builder.add_edge("multiQueryExpansion", "hybridCC")
builder.add_edge("hybridCC", "cohereRerank")
builder.add_edge("cohereRerank", "generateAnswer")
builder.add_edge("generateAnswer", "merge")
builder.add_edge("merge", END)

graph = builder.compile()