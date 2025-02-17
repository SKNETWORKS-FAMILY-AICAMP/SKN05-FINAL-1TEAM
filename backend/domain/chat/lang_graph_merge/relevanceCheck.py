from langgraph.types import StreamWriter
from domain.chat.lang_graph_merge.state import OverallState
from domain.chat.lang_graph_merge.setup import UpsateGC

def relevance_check(state: OverallState, writer: StreamWriter):

    writer(
        {
            "currentNode": "답변 검증",
            "answer": "",
            "keywords": [],
            "suggestQuestions": [],
            "sessionId": state.get("sessionId"),
            "messageId": state.get("messageId"),
        }
    )

    docs = state["context"]
    context = ""
    for i in docs:
        context += i.page_content
        context += "\n"
    answer = state["answer"]

    upstage_ground_checker = UpsateGC()
    request_input = {
    "context": context,
    "answer": answer,
    }
    relevance = upstage_ground_checker.invoke(request_input)
    print(relevance)
    return {"relevance" : relevance}