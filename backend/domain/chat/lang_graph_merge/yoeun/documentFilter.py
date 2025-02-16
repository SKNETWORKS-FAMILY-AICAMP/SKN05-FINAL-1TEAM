# import torch
import numpy as np
import gc
from langgraph.types import StreamWriter
from domain.chat.lang_graph_merge.yoeun.state import CanonState
from domain.chat.lang_graph_merge.yoeun.setup import filter_embedding_model


# def assign_embedding_similarity_score(docs, query_embedding):
#     doc_embeddings = [filter_embedding_model().encode(doc.page_content) for doc in docs]
#     scores = [np.dot(query_embedding, doc_embedding) for doc_embedding in doc_embeddings]
#     return list(zip(docs, scores))

# 특정 키워드 기반 Percentile 필터링 함수
def filter_documents_by_percentile(docs_with_scores, percentile_cutoff=80):
    scores = [score for _, score in docs_with_scores]
    if not scores:
        return []
    cutoff_value = np.percentile(scores, percentile_cutoff)  # 상위 percentile 계산
    return [doc for doc, score in docs_with_scores if score >= cutoff_value]

def assign_embedding_similarity_score(docs, query_embedding):
    doc_embeddings = []
    
    for doc in docs:
        # with torch.no_grad():
        embedding = filter_embedding_model().encode(doc.page_content)  # 인코딩 수행
        doc_embeddings.append(embedding)  # 결과 리스트에 추가

        # del embedding 
        gc.collect()
            # torch.cuda.empty_cache()  # GPU 캐시 메모리 정리
            # print("cache 정리!")

    scores = [np.dot(query_embedding, doc_embedding) for doc_embedding in doc_embeddings]
    return list(zip(docs, scores))

def filter_document(state: CanonState, writer: StreamWriter) -> CanonState:
    writer(
        {
            "currentNode": "문서 선별 중",
            "answer": "",
            "keywords": [],
            "suggestQuestions": [],
            "sessionId": state.get("sessionId"),
            "messageId": state.get("messageId"),
        }
    )
    print("---[CANON]DOCUMENT FILTERING---")
    # Query 및 문서 임베딩 생성
    query = state['question']
    docs = state['ensemble_context']
    query_embedding = filter_embedding_model().encode(query)
    docs_with_scores = assign_embedding_similarity_score(docs, query_embedding)
    filtered_docs = filter_documents_by_percentile(docs_with_scores, percentile_cutoff=80)
    print(f"필터링 전 문서 : {len(docs)} / 필터링 후 문서 : {len(filtered_docs)}")
    return {"filtered_context": filtered_docs}