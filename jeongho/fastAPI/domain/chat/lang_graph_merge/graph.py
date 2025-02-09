from langgraph.graph import StateGraph
from langchain_core.runnables import RunnableLambda
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from domain.chat.lang_graph_merge.state import OverallState, InputState
from domain.chat.lang_graph_merge.check_validation_criteria import check_validation_criteria
from domain.chat.lang_graph_merge.decide_next_step import decide_next_step
from domain.chat.lang_graph_merge.refine_question_node import refine_question
from domain.chat.lang_graph_merge.not_for_camera import not_for_camera
from domain.chat.lang_graph_merge.settings_generate import settings_generate
from domain.chat.lang_graph_merge.relevanceCheck import relevance_check
from domain.chat.lang_graph_merge.keywordExtract import keyword_extract
from domain.chat.lang_graph_merge.queryRewrite import query_rewrite
from domain.chat.lang_graph_merge.suggestQuestion import suggest_question

from domain.chat.lang_graph_merge.jeongho.graph import subgraph
from domain.chat.lang_graph_merge.yoeun.graph import subgraph_canon

from domain.chat.lang_graph_merge.conditional_routing import conditional_routing
from domain.chat.lang_graph_merge.relevance_routing import relevance_routing


fuji = subgraph
canon = subgraph_canon

def sony(state):
    pass

# 그래프 초기화
graph = StateGraph(OverallState, input=InputState)

# 노드 추가
graph.add_node("validate_input", check_validation_criteria)
graph.add_node("decide_next_step", decide_next_step)
graph.add_node("ask_brand", refine_question)
graph.add_node("not_for_camera", not_for_camera)
graph.add_node("settings_generate", settings_generate)

graph.add_node("fuji", fuji)
graph.add_node("canon", canon)
graph.add_node("sony", sony)

graph.add_node("relevance_check", relevance_check)
graph.add_node("keyword_extract", keyword_extract)
graph.add_node("query_rewrite", query_rewrite)
graph.add_node("suggest_questions", suggest_question)

# 엣지 추가
graph.add_edge(START, 'validate_input')
graph.add_edge("validate_input", "decide_next_step")
graph.add_conditional_edges(
    "decide_next_step", 
    conditional_routing, 
    {
        "ask_brand": "ask_brand", 
        "not_for_camera": "not_for_camera", 
        "settings_generate": "settings_generate",
        "rag_fuji": "fuji",
        "rag_canon": "canon",
        "rag_sony": "sony"      
        }
)
graph.add_edge("ask_brand", "decide_next_step")
graph.add_edge("not_for_camera", END)
graph.add_edge("settings_generate","decide_next_step")
graph.add_edge("fuji","relevance_check")
graph.add_edge("canon","relevance_check")

graph.add_conditional_edges(
    "relevance_check", 
    relevance_routing, 
    {
        "keyword_extract": "keyword_extract", 
        "query_rewrite": "query_rewrite",   
        }
)

graph.add_conditional_edges(
    "query_rewrite", 
    conditional_routing, 
    {
        "rag_fuji": "fuji",
        "rag_canon": "canon",
        "rag_sony": "sony"      
        }
)

graph.add_edge("keyword_extract", "suggest_questions")
graph.add_edge("suggest_questions",END)



# graph.add_edge(START, 'validate_input')
# graph.add_edge("validate_input", "decide_next_step")

# graph.add_conditional_edges(
#     "decide_next_step", 
#     conditional_routing, 
#     {
#         "ask_brand": "ask_brand", 
#         "not_for_camera": "not_for_camera", 
#         "settings_generate": "settings_generate",
#         "rag_fuji": "fuji",
#         "rag_canon": "canon",
#         "rag_sony": "sony"      
#         }
# )

# graph.add_edge("ask_brand", "decide_next_step")
# graph.add_edge("not_for_camera", END)
# graph.add_edge("settings_generate","decide_next_step")
# graph.add_edge("fuji","relevance_check")
# graph.add_edge("canon","relevance_check")
# graph.add_edge("sony","relevance_check")

# graph.add_conditional_edges(
#     "relevance_check", 
#     relevance_routing, 
#     {
#         "keyword_extract": "keyword_extract", 
#         "query_rewrite": "query_rewrite",   
#         }
# )

# graph.add_conditional_edges(
#     "query_rewrite", 
#     conditional_routing, 
#     {
#         "rag_fuji": "fuji",
#         "rag_canon": "canon",
#         "rag_sony": "sony"      
#         }
# )

# graph.add_edge("keyword_extract", "suggest_questions")
# graph.add_edge("suggest_questions",END)

memory=  MemorySaver()

app = graph.compile(checkpointer=memory)