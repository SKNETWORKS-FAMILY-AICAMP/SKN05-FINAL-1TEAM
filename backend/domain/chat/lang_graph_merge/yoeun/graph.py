from langgraph.graph import START, END, StateGraph
from domain.chat.lang_graph_merge.yoeun.state import CanonState
from domain.chat.lang_graph_merge.state import OverallState
from domain.chat.lang_graph_merge.yoeun.multiQuery import query_expansion
from domain.chat.lang_graph_merge.yoeun.retrieve import ensemble_document, duplicated_delete, document_search
from domain.chat.lang_graph_merge.yoeun.documentFilter import filter_document
from domain.chat.lang_graph_merge.yoeun.rerank import rerank_docs
from domain.chat.lang_graph_merge.yoeun.generate import generate


canongraph = StateGraph(CanonState, input=OverallState)
canongraph.add_node("query_expansion", query_expansion)
canongraph.add_node("ensemble_retriever", ensemble_document)
canongraph.add_node("merge_document", duplicated_delete)
canongraph.add_node("filter", filter_document)
canongraph.add_node("reranker", rerank_docs)
canongraph.add_node("generate", generate)

canongraph.add_edge(START, "query_expansion")
canongraph.add_conditional_edges("query_expansion", document_search, ["ensemble_retriever"])
canongraph.add_edge("ensemble_retriever", "merge_document")
# canongraph.add_edge("merge_document", "reranker")

canongraph.add_edge("merge_document", "filter")
canongraph.add_edge("filter", "reranker")
canongraph.add_edge("reranker", "generate")
canongraph.add_edge("generate", END)

subgraph_canon = canongraph.compile()