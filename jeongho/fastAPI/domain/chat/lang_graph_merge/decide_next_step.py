# 조건에 따른 다음 단계 결정
from langgraph.types import StreamWriter
from domain.chat.lang_graph_merge.state import RouterState


def decide_next_step(state: RouterState, writer: StreamWriter) -> RouterState:
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
    brand = state.get('brand', None)
    validation_results = state["validation_results"]
    
    if all(validation_results.values()):
        if brand == 'canon':
            next_step = "rag_canon" # subgraph
        elif brand == 'sony':
            next_step = "rag_sony" # subgraph
        elif brand == 'fuji':
            next_step = "rag_fuji" # subgraph
    else:
        if not validation_results["camera_question"]:
            next_step = "not_for_camera" # 카메라 관련 질문이 아니다 답변 노드
        elif not validation_results["choose_brand"]:
            next_step = "ask_brand" # 역질문 노드
        elif not validation_results["is_setting"]:
            next_step = "settings_generate" # 사용자 메뉴얼 관련 답변 및 질문 재생성 노드
    return {
        **state,
        "next_step": next_step
    }