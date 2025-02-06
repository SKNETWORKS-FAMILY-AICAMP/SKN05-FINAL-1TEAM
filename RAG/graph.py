from langgraph.graph import StateGraph, END, START
from langchain_core.runnables import RunnableLambda
from langgraph.checkpoint.memory import MemorySaver

from state import OverallState, InputState, OutputState
from node.queryClassifier import check_validation_criteria, decide_next_step
from node.subgraph.graph import subgraph_canon
from node.generate_all import generate_all
from node.relevance_check import relevance_check
from node.queryRewrite import query_rewrite
from node.keyworExtract import keyword_extract
from node.suggestQuestion import suggest_question


# 그래프 초기화
graph = StateGraph(OverallState, input=InputState, output=OutputState)

# 노드 추가
graph.add_node("validate_input", RunnableLambda(check_validation_criteria))
graph.add_node("decide_next_step", RunnableLambda(decide_next_step))
# graph.add_node("ask_brand", RunnableLambda(refine_question))
graph.add_node("rag_any", RunnableLambda(generate_all))
graph.add_node("rag_canon", subgraph_canon)
graph.add_node("relevance_check", RunnableLambda(relevance_check))
graph.add_node("rewrite_query", RunnableLambda(query_rewrite))
graph.add_node("keyword_extract", RunnableLambda(keyword_extract))
graph.add_node("suggest_questions", RunnableLambda(suggest_question))


def conditional_routing(state):
    next_step = state.get("next_step", "END")
    if next_step not in ["rag_any", "rag_canon"]:
        return [END]
    
    return [next_step]

def relevance_routing(state):
    relevance = state.get("relevance","rewrite_query")
    if relevance == "grounded":
        return ["keyword_extract"]
    return ["rewrite_query"]

# 엣지 추가
graph.add_edge(START, 'validate_input')
graph.add_edge("validate_input", "decide_next_step")
graph.add_conditional_edges("decide_next_step", conditional_routing, ["rag_any","rag_canon",END])

graph.add_edge("rag_any", "relevance_check")
graph.add_edge("rag_canon","relevance_check")
graph.add_conditional_edges("relevance_check",relevance_routing, ["keyword_extract","rewrite_query"])
graph.add_conditional_edges("rewrite_query", conditional_routing, ["rag_any","rag_canon"])
graph.add_edge("keyword_extract","suggest_questions")
graph.add_edge("suggest_questions",END)


memory=MemorySaver()

app=graph.compile(checkpointer=memory)