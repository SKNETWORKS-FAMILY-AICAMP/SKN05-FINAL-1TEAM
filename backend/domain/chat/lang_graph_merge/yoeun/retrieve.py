from langgraph.types import Send
from langchain.retrievers import EnsembleRetriever


from domain.chat.lang_graph_merge.yoeun.state import CanonState, QueryState
from domain.chat.lang_graph_merge.yoeun.setup import vector_store, bm25_retriever


# Ensemble retriever + Map reduce
def ensemble_document(state: CanonState):
    print("---[CANON] ENSEMBLE RETRIEVE---")

    questions = state["question"]
    model = state.get("model")

    mapping_model = {
    "EOS R6" : "R6",
    "EOS R50 Mark II" : "R50",
    "EOS M50 Mark II" : "M50",
    "PowerShot G7X Mark III" : "G7X",
    "EOS 200D II" : "200D"   
    }

    # print(f"질문 : {questions}, 모델 : {model}")
    print(f"질문 : {questions}")
    search_kwargs = {"k": 10}

    if model:
        change_model = mapping_model.get(model, None)
        search_kwargs["filter"] = {"model": change_model}

    print(search_kwargs)
    pinecone_retriever = vector_store.as_retriever(
        search_type="similarity", search_kwargs=search_kwargs
    )

    # filtered_bm25_retriever = FilteredBM25Retriever.from_documents(bm25_retriever.docs, model_filter=model, preprocess_func=kiwi_tokenize)
    ensemble_retriever = EnsembleRetriever(retrievers=[pinecone_retriever, bm25_retriever], weights=[0.5, 0.5])
    documents = ensemble_retriever.invoke(questions)
    if model:
        documents = [doc for doc in documents if doc.metadata.get("model") == change_model]

    # print("------처음 docs-------")
    # print(documents)
    # print("------filter docs-------")
    print(documents)

    return {"multi_context": documents}

def document_search(state: CanonState):
    requests = []
    for q in state["transform_question"]:
        data = {"question": q}
        if state.get("model"):  # 🔥 모델이 존재하면 추가
            data["model"] = state["model"]
        requests.append(Send("ensemble_retriever", data))
    return requests

def duplicated_delete(state: CanonState) -> CanonState:
    print("---[CANON] MERGE DOCUMENT---")
    documents = state['multi_context']
    seen_ids = set()
    merge_results = []
    for item in documents:
        if item.id not in seen_ids:
            merge_results.append(item)
            seen_ids.add(item.id)
    return {"ensemble_context": merge_results}