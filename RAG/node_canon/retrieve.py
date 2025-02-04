from state import GraphState
from ingestion import retriever, ensemble_retriever, bm25_retriever

# 기본 Retrieve document 정의
# def retrieve_document(state: GraphState) -> GraphState:
#     print("---RETRIEVE---")
#     questions = state["question"]
#     documents = retriever.invoke(questions)
#     print(documents)
#     return {"context": documents, "question": questions}

# Ensemble retriever 정의
def ensemble_document(state: GraphState) -> GraphState:
    print("---ENSEMBLE RETRIEVE---")
    questions = state["question"]
    documents = ensemble_retriever.invoke(questions)
    # print(documents)
    return {"ensemble_context": documents}