# querymerge.py
from state import GraphState


def merge_results(state: GraphState) -> GraphState:
    print("---MERGE---")

    multi_query_result = state['multi_context']
    ensemble_result = state['ensemble_context']
    # print(multi_query_result)
    # print(ensemble_result)

    # 중복 제거 (예: 문서 ID 기준)
    seen_ids = set()
    merged_result = []

    for item in multi_query_result + ensemble_result:
        if item.id not in seen_ids:
            merged_result.append(item)
            seen_ids.add(item.id)
    # print(state)

    return {'merge_context': merged_result}
