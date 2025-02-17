from langgraph.types import StreamWriter
from domain.chat.lang_graph_merge.hyeseo.state import SonyState


def duplicated_delete(state: SonyState, writer: StreamWriter):
    documents = state['filtered_context']
    seen_ids = set()
    merge_results = []
    for item in documents:
        if item.id not in seen_ids:
            merge_results.append(item)
            seen_ids.add(item.id)
    return {"ensemble_context": merge_results}