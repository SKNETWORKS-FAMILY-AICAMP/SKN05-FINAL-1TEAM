from state import GraphState
from ingestion import filter_embedding_model

import numpy as np

# 특정 키워드 기반 Percentile 필터링 함수
def filter_documents_by_percentile(docs_with_scores, percentile_cutoff=80):
    scores = [score for _, score in docs_with_scores]

    if not scores:
        return []

    cutoff_value = np.percentile(scores, percentile_cutoff)  # 상위 percentile 계산
    return [doc for doc, score in docs_with_scores if score >= cutoff_value]

def assign_embedding_similarity_score(docs, query_embedding):
    doc_embeddings = [filter_embedding_model.encode(doc.page_content) for doc in docs]
    
    # Dot Product로 유사도 점수 계산
    scores = [np.dot(query_embedding, doc_embedding) for doc_embedding in doc_embeddings]

    return list(zip(docs, scores))


def filter_document(state: GraphState) -> GraphState:
    print("---DOCUMENT FILTERING---")
    # Query 및 문서 임베딩 생성
    query = state['question']
    docs = state['merge_context']

    query_embedding = filter_embedding_model.encode(query)
    # Embedding 기반 유사도 점수 계산
    docs_with_scores = assign_embedding_similarity_score(docs, query_embedding)
    # Percentile Cutoff 적용 (상위 80%)
    filtered_docs = filter_documents_by_percentile(docs_with_scores, percentile_cutoff=80)
    print(f"필터링 전 문서 : {len(docs)} / 필터링 후 문서 : {len(filtered_docs)}")
    return {"filtered_context": filtered_docs}