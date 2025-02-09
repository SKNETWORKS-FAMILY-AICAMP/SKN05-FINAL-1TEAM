## router 관련 함수
from langchain_core.output_parsers import BaseOutputParser
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from typing import Dict, List

from temp_state import InputState, RouterState
import json


# output 정의
class ListOutputParser(BaseOutputParser[List[str]]):
    def parse(self, text: str) -> List[str]:
        if isinstance(text, AIMessage):
            text = text.content
        
        try:
            parsed_json = json.loads(text)
            return parsed_json
        except:
            lines = text.replace("[", "").replace("]","").strip().split(",")
            return list(filter(None, lines))
        # return list(filter(None, lines))  # Remove empty lines

# output 정의
def parse_validation_results(parsed_json: list) -> Dict[str, bool]:
    """ LLM 응답을 리스트로 변환 후 Dict로 매핑 """
    # try:
    #     parsed_json = json.loads(text)  # JSON 형식이면 바로 변환
    # except:
    #     parsed_json = list(filter(None, text.strip().split("\n")))  # 개행 문자 기준으로 분리 후 빈 값 제거
        
    return {
        "camera_question": parsed_json[0] == "TRUE",
        "is_setting": parsed_json[1] == "TRUE",
        "choose_brand": parsed_json[2] == "TRUE"
    }
parse_lambda = RunnableLambda(parse_validation_results)  # LCEL에서 Lambda로 실행


# 검증 기준 체크하는 함수
def check_validation_criteria(state: InputState) -> RouterState:
    question = state['question']
    brand = state.get('brand', None)  # 선택적 필드는 `.get()` 사용
    model = state.get('model', None)  # 선택적 필드

    llm = ChatOpenAI(temperature=0, model_name="gpt-4o")
    
    # 검증 템플릿
    validation_prompt = ChatPromptTemplate.from_template("""
    다음은 사용자의 질문과 선택한 브랜드 및 모델 정보입니다. 이 정보를 바탕으로 세 가지 사항을 판단하세요. 각 판단은 TRUE 또는 FALSE로 리스트 형태로 반환합니다.

    1. 사용자의 질문이 카메라에 대한 질문인지 판단하세요.
    2. 사용자의 질문에 카메라 사용자 메뉴얼에 대한 내용이 포함되어 있는지 판단하세요.(카메라 설정, 기능, 안전 유의사항 등)
    3. 제공된 정보에 브랜드와 모델이 포함되어 있는지, 사용자가 선택한 내용과 질문 모두에서 확인하세요.

    사용자 질문: {question}
    선택한 브랜드: {brand}
    선택한 모델: {model}

    판단 결과를 [TRUE, FALSE, FALSE] 형식으로 반환하세요.
    """)

    # LCEL 기반 실행 체인
    llm_chain = (
        validation_prompt| llm | ListOutputParser() | parse_lambda
    )
    
    # 검증 실행
    validation_results = llm_chain.invoke({"question": question, "brand": brand, "model": model})

    return {
        **state,
        "validation_results": validation_results
    }

# 조건에 따른 다음 단계 결정
def decide_next_step(state: RouterState) -> RouterState:
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
    
    # print(next_step)
    return {
        "next_step": next_step
    }