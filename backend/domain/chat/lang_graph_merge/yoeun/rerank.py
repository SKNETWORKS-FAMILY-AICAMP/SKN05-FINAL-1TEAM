from langgraph.types import StreamWriter
from domain.chat.lang_graph_merge.yoeun.state import CanonState
from domain.chat.lang_graph_merge.yoeun.setup import yoeun_cohere

def rerank_with_cohere(query, retrieved_docs, top_n=5):
    documents = [doc.page_content for doc in retrieved_docs]
    cohere_client = yoeun_cohere()
    response = cohere_client.rerank(
        query=query,
        documents=documents,
        top_n=top_n,
        model="rerank-v3.5"
    )
    reranked_docs = [retrieved_docs[result.index] for result in response.results]
    return reranked_docs

# Reranker Node
def rerank_docs(state: CanonState, writer: StreamWriter) -> CanonState:
    writer(
        {
            "currentNode": "문서 정렬 중",
            "answer": "",
            "keywords": [],
            "suggestQuestions": [],
            "sessionId": state.get("sessionId"),
            "messageId": state.get("messageId"),
        }
    )
    print("---[CANON] RERANK---")
    questions = state['question']
    documents = state['filtered_context']
    reranked_docs = rerank_with_cohere(questions, documents)
    print(reranked_docs)
    return {"context": reranked_docs}