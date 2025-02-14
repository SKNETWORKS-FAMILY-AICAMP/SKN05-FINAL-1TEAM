from langgraph.graph import StateGraph, START, END
from domain.chat.lang_graph_merge.hyeseo.state import SonyState
from domain.chat.lang_graph_merge.hyeseo.multiquery import q
from domain.chat.lang_graph_merge.hyeseo.state import SonyState
from domain.chat.lang_graph_merge.hyeseo.state import SonyState
from domain.chat.lang_graph_merge.hyeseo.state import SonyState
from domain.chat.lang_graph_merge.hyeseo.state import SonyState
from domain.chat.lang_graph_merge.hyeseo.state import SonyState
from domain.chat.lang_graph_merge.hyeseo.state import SonyState

sonygraph = StateGraph(SonyState)

sonygraph.add_node("query_expansion", query_expansion)
sonygraph.add_node("ensemble_retriever", ensemble_document)
sonygraph.add_node("filter", filter_document)
sonygraph.add_node("reranker", rerank_docs)
sonygraph.add_node("generate", generate)


# 🔹 **Graph 연결 (Flow 설정)**

sonygraph.add_edge(START, "query_expansion")  # 시작 → Query 확장
sonygraph.add_conditional_edges("query_expansion", document_search, ["ensemble_retriever"])  # 검색 수행
sonygraph.add_edge("ensemble_retriever", "merge_document")  # 검색 결과 → 중복 제거
# sonygraph.add_edge("merge_document", "reranker")  # 기존 주석 처리됨

sonygraph.add_edge("merge_document", "filter")  # 중복 제거 후 필터링 적용
sonygraph.add_edge("filter", "reranker")  # 필터링 → 재정렬
sonygraph.add_edge("reranker", "generate")  # 재정렬 → 답변 생성
sonygraph.add_edge("generate", END)  # 답변 생성 후 종료


# 🔹 **최종 그래프 컴파일**
subgraph_sony = sonygraph.compile()