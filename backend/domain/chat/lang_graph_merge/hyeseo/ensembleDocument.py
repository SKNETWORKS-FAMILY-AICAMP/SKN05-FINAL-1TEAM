from langgraph.types import StreamWriter, Send
from domain.chat.lang_graph_merge.hyeseo.state import SonyState
from domain.chat.lang_graph_merge.hyeseo.setup import ensemble_retriever


def document_search(state: SonyState):
    return [Send("ensemble_retriever", {"question": q}) for q in state["transform_question"]]


def ensemble_document(state: SonyState, writer: StreamWriter):
    writer(
        {
            "currentNode": "ensemble_document(확인을 위한 출력)",
            "answer": "",
            "keywords": [],
            "suggestQuestions": [],
            "sessionId": state.get("sessionId"),
            "messageId": state.get("messageId"),
        }
    )
    print("---[SONY] ENSEMBLE RETRIEVE---")
    questions = state["question"]
    print(f"질문 : {questions}")
    documents = ensemble_retriever().invoke(questions)
    return {"multi_context": documents}