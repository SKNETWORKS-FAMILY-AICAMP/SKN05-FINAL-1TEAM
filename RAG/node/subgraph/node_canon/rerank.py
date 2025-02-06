from node.subgraph.state import CanonState
from node.subgraph.ingestion import cohere_client

def rerank_with_cohere(query, retrieved_docs, top_n=5):
    documents = [doc.page_content for doc in retrieved_docs]
    response = cohere_client.rerank(
        query=query,
        documents=documents,
        top_n=top_n,
        model="rerank-v3.5"
    )
    reranked_docs = [retrieved_docs[result.index] for result in response.results]
    return reranked_docs

# Reranker Node
def rerank_docs(state: CanonState) -> CanonState:
    print("---[CANON] RERANK---")
    questions = state['question']
    documents = state['filtered_context']
    reranked_docs = rerank_with_cohere(questions, documents)
    print(reranked_docs)
    return {"context": reranked_docs}