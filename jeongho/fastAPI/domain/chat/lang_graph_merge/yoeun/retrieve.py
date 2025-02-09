from langgraph.types import Send
from domain.chat.lang_graph_merge.yoeun.state import CanonState, QueryState
from domain.chat.lang_graph_merge.yoeun.setup import ensemble_retriever


# Ensemble retriever + Map reduce
def ensemble_document(state: QueryState):
    print("---[CANON] ENSEMBLE RETRIEVE---")
    questions = state["question"]
    print(f"질문 : {questions}")
    documents = ensemble_retriever().invoke(questions)
    # print(documents)
    return {"multi_context": documents}

def document_search(state: CanonState):
    return [Send("ensemble_retriever", {"question": q}) for q in state["transform_question"]]

def duplicated_delete(state: CanonState) -> CanonState:
    documents = state['multi_context']
    seen_ids = set()
    merge_results = []
    for item in documents:
        if item.id not in seen_ids:
            merge_results.append(item)
            seen_ids.add(item.id)
    return {"ensemble_context": merge_results}