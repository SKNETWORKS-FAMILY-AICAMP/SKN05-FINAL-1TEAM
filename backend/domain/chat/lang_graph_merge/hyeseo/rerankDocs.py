from langgraph.types import StreamWriter
from domain.chat.lang_graph_merge.hyeseo.state import SonyState
from domain.chat.lang_graph_merge.hyeseo.setup import hyeseo_cohere


def rerank_with_cohere(query, retrieved_docs, top_n=5):
    documents = [doc.page_content for doc in retrieved_docs]
    cohere_client = hyeseo_cohere()
    response = cohere_client.rerank(
        query=query,
        documents=documents,
        top_n=top_n,
        model="rerank-v3.5"
    )
    reranked_docs = [retrieved_docs[result.index] for result in response.results]
    return reranked_docs

def rerank_docs(state: SonyState, writer: StreamWriter) -> SonyState:
    writer(
        {
            "currentNode": "rerank_docs(확인을 위한 출력)",
            "answer": "",
            "keywords": [],
            "suggestQuestions": [],
            "sessionId": state.get("sessionId"),
            "messageId": state.get("messageId"),
        }
    )
    print("---[SONY] RERANK---")
    questions = state['question']
    documents = state['ensemble_context']
    reranked_docs = rerank_with_cohere(questions, documents)
    print(reranked_docs)
    return {"rerank_context": reranked_docs}