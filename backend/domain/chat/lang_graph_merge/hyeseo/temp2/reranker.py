
# from state import GraphState
# from ingestion import cohere_client


def rerank_with_cohere(query, retrieved_docs, top_n=5):
    # Cohere에 전달할 문서 형식
    documents = [doc.page_content for doc in retrieved_docs]
    
    # Reranker 호출a
    
    response = cohere_client.rerank(
        query=query,
        documents=documents,
        top_n=top_n,  # 상위 N개 문서 선택
        model="rerank-v3.5"  # 사용할 Cohere Reranker 모델
    )
    
    # 상위 문서만 반환
    reranked_docs = [retrieved_docs[result.index] for result in response.results]
    return reranked_docs

# Reranker Node
def rerank_docs(state: GraphState) -> GraphState:
    
    questions = state['question']
    documents = state['merge_context']
    reranked_docs = rerank_with_cohere(questions, documents)
    return {"rerank_context": reranked_docs}