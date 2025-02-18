# import torch
import numpy as np
import gc
from openai import OpenAI
from langgraph.types import StreamWriter
from domain.chat.lang_graph_merge.yoeun.state import CanonState
from domain.chat.lang_graph_merge.yoeun.setup import embedding_data
from domain.chat.lang_graph_merge.yoeun.setup import load_yoeun_dotenv

load_yoeun_dotenv()
client = OpenAI()

# 특정 키워드 기반 Percentile 필터링 함수
def get_embedding_by_id(doc_id):
    for item in embedding_data:
        if item['id'] == doc_id:
            return np.array(item["values"])
    return None

# 쿼리 임베딩 생성 함수
def generate_embeddings(query):
    response = client.embeddings.create(input=query, model="text-embedding-3-small")
    embeddings = response.data[0].embedding
    return embeddings

def filter_documents_by_percentile(docs_with_scores, percentile_cutoff=80):
    scores = [score for _, score in docs_with_scores]
    if not scores:
        return []
    cutoff_value = np.percentile(scores, percentile_cutoff)  # 상위 percentile 계산
    return [doc for doc, score in docs_with_scores if score >= cutoff_value]

def assign_embedding_similarity_score(docs, query_embedding):
    docs_with_scores = []
    
    for doc in docs:
        doc_id = doc.id
        doc_embedding = get_embedding_by_id(doc_id)

        if doc_embedding is not None:
            score = np.dot(query_embedding, doc_embedding)
            docs_with_scores.append((doc, score))

        gc.collect()

    return docs_with_scores

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
    # Query 및 문서 임베딩 생성
    query = state['question']
    docs = state['ensemble_context']
    query_embedding = generate_embeddings(query)

    docs_with_scores = assign_embedding_similarity_score(docs, query_embedding)
    filtered_docs = filter_documents_by_percentile(docs_with_scores, percentile_cutoff=80)
    print(f"필터링 전 문서 : {len(docs)} / 필터링 후 문서 : {len(filtered_docs)}")
    return {"filtered_context": filtered_docs}
