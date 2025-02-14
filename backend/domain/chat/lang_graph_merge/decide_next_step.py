# 조건에 따른 다음 단계 결정
from langgraph.types import StreamWriter
from domain.chat.lang_graph_merge.state import RouterState


def decide_next_step(state: RouterState, writer: StreamWriter) -> RouterState:
    writer(
        {
            "currentNode": "decide_next_step(확인을 위한 출력)",
            "answer": "",
            "keywords": [],
            "suggestQuestions": [],
            "sessionId": state.get("sessionId"),
            "messageId": state.get("messageId"),
        }
    )
    writer(
        {
            "currentNode": "질문 분석 중",
            "answer": "",
            "keywords": [],
            "suggestQuestions": [],
            "sessionId": state.get("sessionId"),
            "messageId": state.get("messageId"),
        }
    )
    return {"next_step": state.get("next_step", None)}