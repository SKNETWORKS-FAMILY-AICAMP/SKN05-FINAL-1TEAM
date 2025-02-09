from domain.chat.lang_graph_merge.state import RouterState, OutputState


def not_for_camera(state:RouterState) -> OutputState:
    question= state["question"]
    answer = f"{question} 내용은 카메라에 대한 질문이 아니라 답변할 수 없습니다."

    message = [{"role": "user", "content": question},{"role":"assistant", "content":answer}]
    return {"answer": answer, "message": message}