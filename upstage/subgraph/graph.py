# 🔹 Sony Graph 정의 및 파이프라인 구성
sonygraph = GraphState(SonyState)

# 1. 프롬프트 확장 (Query Expansion)
sonygraph.add_node("query_expansion", query_expansion)

# 2. 검색기 (Ensemble Retriever - BM25 + Pinecone Hybrid)
sonygraph.add_node("ensemble_retriever", ensemble_document)

# sonygraph.add_node("merge_document", duplicated_delete)

sonygraph.add_node("filter", filter_document)

sonygraph.add_node("reranker", rerank_docs)

# 6. 답변 생성 (Final Answer Generation)
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