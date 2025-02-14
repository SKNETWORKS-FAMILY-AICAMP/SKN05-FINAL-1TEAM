from langgraph.types import StreamWriter
from domain.chat.lang_graph_merge.hyeseo.state import SonyState


def duplicated_delete(state: SonyState, writer: StreamWriter):
    writer(
        {
            "currentNode": "duplicated_delete(확인을 위한 출력)",
            "answer": "",
            "keywords": [],
            "suggestQuestions": [],
            "sessionId": state.get("sessionId"),
            "messageId": state.get("messageId"),
        }
    )
    documents = state['multi_context']
    seen_ids = set()
    merge_results = []
    for item in documents:
        if item.id not in seen_ids:
            merge_results.append(item)
            seen_ids.add(item.id)
    return {"ensemble_context": merge_results}