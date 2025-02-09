from langgraph.graph import StateGraph, START, END

from temp_state import InputState, OverallState, RouterState
from langgraph.checkpoint.memory import MemorySaver
from router import check_validation_criteria, decide_next_step
from reverseQuestion import human_node
from temp_generate import generate_answer

builder = StateGraph(RouterState, input=InputState)

builder.add_node(check_validation_criteria, "check_validation_criteria")
builder.add_node(decide_next_step, "decide_next_step")
builder.add_node(human_node, "human_node")
builder.add_node(generate_answer, "generate_answer")

builder.add_edge(START, "check_validation_criteria")
builder.add_edge("check_validation_criteria", "decide_next_step")
builder.add_edge("decide_next_step", "human_node")
builder.add_edge("human_node", "generate_answer")
builder.add_edge("generate_answer", END)

memory = MemorySaver()

graph = builder.compile(checkpointer=memory)