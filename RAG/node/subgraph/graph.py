
from dotenv import load_dotenv
from langgraph.graph import START, END, StateGraph


from node.subgraph.state import CanonState
from node.subgraph.node_canon.multiQuery import query_expansion
from node.subgraph.node_canon.retrieve import ensemble_document, duplicated_delete, document_search
from node.subgraph.node_canon.documentFilter import filter_document
from node.subgraph.node_canon.rerank import rerank_docs
from node.subgraph.node_canon.generate import generate

load_dotenv()

canongraph = StateGraph(CanonState)
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