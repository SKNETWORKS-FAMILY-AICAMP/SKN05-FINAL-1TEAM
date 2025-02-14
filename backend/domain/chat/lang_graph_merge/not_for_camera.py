from langgraph.types import StreamWriter
from domain.chat.lang_graph_merge.state import RouterState, OutputState

def not_for_camera(state:RouterState, writer:StreamWriter) -> OutputState:
    question= state["question"]


    answer = f'''"{question}" 내용은 카메라에 대한 질문이 아니라 답변할 수 없습니다.'''

    writer(
        {
            "currentNode": "not_for_camera",
            "answer": answer,
            "keywords": [],
            "suggestQuestions": [],
            "sessionId": state.get("sessionId"),
            "messageId": state.get("messageId"),
        }
    )
    # message = [{"role": "user", "content": question},{"role":"assistant", "content":answer}]
    return {"answer": answer}






