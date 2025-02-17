from langgraph.graph import START, END, StateGraph
from domain.chat.lang_graph_merge.hyeseo.state import SonyState
from domain.chat.lang_graph_merge.hyeseo.queryExpansion import query_expansion
from domain.chat.lang_graph_merge.hyeseo.ensembleDocument import ensemble_document, document_search
from domain.chat.lang_graph_merge.hyeseo.duplicatedDelete import duplicated_delete
from domain.chat.lang_graph_merge.hyeseo.rerankDocs import rerank_docs
from domain.chat.lang_graph_merge.hyeseo.generate import generate
from domain.chat.lang_graph_merge.hyeseo.modelfiltering import filter_manuals 


sonygraph = StateGraph(SonyState)

sonygraph.add_node("query_expansion", query_expansion)
sonygraph.add_node("ensemble_retriever", ensemble_document)
sonygraph.add_node("filter_manuals", filter_manuals)  # 필터링 노드 추가
sonygraph.add_node("merge_document", duplicated_delete)
sonygraph.add_node("reranker", rerank_docs)
sonygraph.add_node("generate", generate)

sonygraph.add_edge(START, "query_expansion")
sonygraph.add_conditional_edges("query_expansion", document_search, ["ensemble_retriever"])
sonygraph.add_edge("ensemble_retriever", "filter_manuals")  # 필터링 추가
sonygraph.add_edge("filter_manuals", "merge_document")  # 필터링 후 중복 제거
sonygraph.add_edge("merge_document", "reranker")
sonygraph.add_edge("reranker", "generate")
sonygraph.add_edge("generate", END)

subgraph_sony = sonygraph.compile()