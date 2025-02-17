from typing import List, Dict
from domain.chat.lang_graph_merge.hyeseo.state import SonyState

# :white_check_mark: 특정 모델의 매뉴얼을 필터링하는 함수
def filter_manuals_by_model(data: List[Dict], model_name: str) -> List[Dict]:
    """특정 카메라 모델의 매뉴얼만 필터링"""
    return [item for item in data if item.metadata.get("model") == model_name]

# :white_check_mark: 필터링 노드
def filter_manuals(state: SonyState) -> SonyState:
    """SonyState 기반으로 필터링 수행"""
    model_name = state.get("model")
    manuals = state.get("multi_context", [])

    filtered_manuals = filter_manuals_by_model(manuals, model_name) if model_name else manuals

    return {**state, "filtered_context": filtered_manuals}