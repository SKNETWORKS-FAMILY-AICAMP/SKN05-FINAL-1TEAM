from state import GraphState

import re

def insert_images(state: GraphState) -> GraphState:
    answer_with_placeholders = state["answer"]
    context = state["rerank_context"]
    
    # 이미지 메타데이터 추출
    image_metadata = context.get("metadata", {}).get("images", {})
    
    # Placeholder를 실제 이미지로 대체
    def replace_placeholder(match):
        placeholder = match.group(0)
        image_path = placeholder.split(":")[1].strip()
        return f"![image]({image_path})"  # Markdown 형식으로 이미지 표시
    
    # 정규식을 사용하여 모든 [이미지 자리: 경로]를 처리
    updated_answer = re.sub(r"\[image:[^\]]+\]", replace_placeholder, answer_with_placeholders)
    
    print("최종 답변:", updated_answer)
    return {"final_answer": updated_answer}