# 검증 기준 체크하는 함수
import json
from typing import Dict
from langgraph.types import StreamWriter
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from domain.chat.lang_graph_merge.state import InputState, RouterState


def parse_validation_results(text: str) -> Dict[str, bool]:
    """ LLM 응답을 리스트로 변환 후 Dict로 매핑 """
    try:
        parsed_json = json.loads(text)  # JSON 형식이면 바로 변환
    except:
        parsed_json = list(filter(None, text.replace("[","").replace("]","").strip().split(",")))  # 개행 문자 기준으로 분리 후 빈 값 제거

    return {
        "camera_question": True,
        "is_setting": True,
        "choose_brand": None
    }
    # return {
    #     "camera_question": parsed_json[0] == "TRUE",
    #     "is_setting": parsed_json[1] == "TRUE",
    #     "choose_brand": parsed_json[2] == "TRUE"
    # }

parse_lambda = RunnableLambda(parse_validation_results)  # LCEL에서 Lambda로 실행

def check_validation_criteria(state: InputState, writer: StreamWriter) -> RouterState:
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
    question = state['question']
    brand = state.get('brand', None)  # 선택적 필드는 `.get()` 사용
    model = state.get('model', None)  # 선택적 필드
    llm = ChatOpenAI(temperature=0, model="gpt-4o")
    
    # 검증 템플릿
    validation_prompt = ChatPromptTemplate.from_template("""
    다음은 사용자의 질문과 선택한 브랜드 및 모델 정보입니다. 이를 바탕으로 세 가지 사항을 판단하세요. 각 판단은 TRUE 또는 FALSE로 리스트 형태로 반환합니다.

    1. 사용자의 질문이 카메라와 관련된 질문인지 판단하세요. (카메라 기기, 기능, 설정, 사용법 등과 관련된 질문이면 TRUE, 아니면 FALSE)
    2. 브랜드 정보를 판단하세요.  
    - 선택한 브랜드가 None이 아니라면 TRUE  
    - 브랜드가 None이지만 질문 내에 브랜드가 언급되어 있다면 TRUE  
    - 위 두 조건에 해당하지 않으면 FALSE  
    3. 모델 정보를 판단하세요.  
    - 선택한 모델이 None이 아니라면 TRUE  
    - 모델이 None이지만 질문 내에 모델이 언급되어 있다면 TRUE  
    - 위 두 조건에 해당하지 않으면 FALSE  

    사용자 질문: {question}  
    선택한 브랜드: {brand}  
    선택한 모델: {model}  

    판단 결과를 [TRUE, TRUE, FALSE] 형식으로 반환하세요.
    """)

    # LCEL 기반 실행 체인
    llm_chain = (
        validation_prompt| llm | StrOutputParser() | parse_lambda  # Dict[str, bool] 형태로 변환
    )
    
    # 검증 실행
    validation_results = llm_chain.invoke({"question": question, "brand": brand, "model": model})
    return {
        **state,
        "validation_results": validation_results
    }
    