# 답변 생성 체인
from state import OverallState
from node.listChain import ListLLMChain

from dotenv import load_dotenv
from typing import Any, Dict
from langchain_core.prompts import PromptTemplate
import asyncio

load_dotenv()
def suggest_question(state: OverallState) -> Dict[str, Any]:
    print("---SUGGEST QUESTION---")
    question = state["question"]
    context = state["context"]
    answer = state['answer']
    SUGGEST_PROMPT = PromptTemplate(
        input_variables=["question","context","answer"],
        template="""
    당신은 카메라 사용자 메뉴얼에 대한 정보를 바탕으로 사용자가 추가로 궁금해할 수 있는 질문을 추천하는 역할을 맡고 있습니다. 아래에 제공된 세 가지 요소를 기반으로, 사용자가 카메라 메뉴얼에서 다시 물어볼 수 있는 추천 질문을 세 가지 생성하세요. 이 질문들은 카메라의 기능, 사용법, 문제 해결 등에 관련된 것이어야 합니다. 출력은 리스트 형태로 제공해주세요.

    1. **Context**: 카메라 사용자 메뉴얼에서 발췌한 정보입니다. 이 정보를 바탕으로 사용자가 추가로 궁금해할 수 있는 부분을 생각해보세요.
    2. **Question**: 사용자가 이미 물어본 질문입니다. 이 질문을 통해 사용자가 어떤 부분에 관심이 있는지 파악하세요.
    3. **Answer**: 위 질문에 대한 답변입니다. 이 답변을 통해 사용자가 이해했을 만한 부분과 추가로 궁금해할 수 있는 부분을 고려하세요.

    예시:
    - Context: [카메라의 ISO 설정 방법에 대한 설명]
    - Question: "ISO 설정을 어떻게 변경하나요?"
    - Answer: "카메라 메뉴에서 ISO 설정을 선택하고 원하는 값을 입력하세요."

    - 추천 질문 리스트: ["ISO 설정이 사진 품질에 미치는 영향은 무엇인가요?", "ISO 설정을 자동으로 조정하는 방법이 있나요?", "ISO 설정 외에 사진의 밝기를 조절할 수 있는 다른 방법은 무엇인가요?"]

    정보:
    **Context**: {context}
    **Question**: {question}
    **Answer**: {answer}
    **Output format: ["추천 질문1","추천 질문2","추천 질문3"]

    위의 정보를 바탕으로 카메라와 관련된 추천 질문을 추출하세요.
    """
    )

    chain = ListLLMChain()

    suggests = chain.run(SUGGEST_PROMPT, {"context": context, "question": question, "answer": answer})
    
    return {"suggest_question" : suggests}
