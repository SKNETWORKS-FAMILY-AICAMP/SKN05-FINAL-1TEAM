from domain.chat.lang_graph_merge.state import OverallState

def temp_node1(state: OverallState) -> OverallState:
    a = state["answer"]
    return {"answer": a}