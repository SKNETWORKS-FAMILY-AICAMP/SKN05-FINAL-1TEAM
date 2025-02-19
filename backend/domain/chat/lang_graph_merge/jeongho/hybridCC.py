import os
import pandas as pd
from langgraph.types import StreamWriter
from domain.chat.lang_graph_merge.jeongho.state import RetrievalState
from domain.chat.lang_graph_merge.jeongho.setup import jeongho_pinecone_index, jeongho_client
from autorag.nodes.retrieval import bm25
from autorag.nodes.retrieval.hybrid_cc import hybrid_cc

client = jeongho_client()

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.join(CURRENT_DIR, "autorag/project_dir")

MODEL = 'text-embedding-3-small'
index = jeongho_pinecone_index()
bm25_retriever = bm25.BM25(project_dir=project_dir, bm25_tokenizer="porter_stemmer")

def hybridCC(state: RetrievalState, writer: StreamWriter) -> RetrievalState:
    writer(
        {
            "currentNode": "문서 검색 중",
            "answer": "",
            "keywords": [],
            "suggestQuestions": [],
            "sessionId": state.get("sessionId"),
            "messageId": state.get("messageId"),
        }
    )

    hybrid_cc_IDs = []
    for queries_from_MQE in state["multi_query_expansion"]:
        df_queries = pd.DataFrame({"query": queries_from_MQE})

        query_results = []

        for query in df_queries["query"]:
            xq = client.embeddings.create(input=query, model=MODEL).data[0].embedding
            query_filter = {"model": {"$eq": state["model"]}} if state.get("model") else None
            query_results.append(index.query(
                xq,
                filter=query_filter,  # 필터가 None이면 적용되지 않음
                top_k=10,
                include_metadata=True
            ))

        semantic_ids = []
        semantic_scores = []
        for single_query_result in query_results:
            single_query_result_ids = []
            single_query_result_scores = []
            for doc_info in single_query_result['matches']:
                single_query_result_ids.append(doc_info['id'])
                single_query_result_scores.append(doc_info['score'])
            semantic_ids.append(single_query_result_ids)
            semantic_scores.append(single_query_result_scores)

        lexical_results_df = bm25_retriever.pure(df_queries, top_k=10, selected_model=state.get("model"))
        lexical_ids = lexical_results_df["retrieved_ids"]
        lexical_scores = lexical_results_df["retrieve_scores"]
        ids = (semantic_ids, lexical_ids)
        scores = (semantic_scores, lexical_scores)
        top_k = 10
        weight = 0.7             # semantic 쪽 가중치 0.7, lexical 쪽 가중치 0.3
        normalize_method = "mm"  # min-max 정규화
        fused_ids, fused_scores = hybrid_cc(
            ids=ids,
            scores=scores,
            top_k=top_k,
            weight=weight,
            normalize_method=normalize_method,
            semantic_theoretical_min_value=-1.0,  # tmm 모드 사용 시 필요한 값
            lexical_theoretical_min_value=0.0     # tmm 모드 사용 시 필요한 값
        )
        hybrid_cc_IDs.append(fused_ids)
    return {"hybrid_cc_IDs": hybrid_cc_IDs}