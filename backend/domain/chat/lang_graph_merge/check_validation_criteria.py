# 검증 기준 체크하는 함수
# import json
# from typing import Dict
from langgraph.types import StreamWriter
# from langchain_openai import ChatOpenAI
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.runnables import RunnableLambda
from domain.chat.lang_graph_merge.state import InputState, RouterState
from domain.chat.lang_graph_merge.setup import load_parent_dotenv


from pydantic import BaseModel
from openai import OpenAI

load_parent_dotenv()
client = OpenAI()

class CameraQuestionAnalysis(BaseModel):
    brand: str | None
    model: str | None
    is_camera_related: bool
    is_manual_related: bool

VALID_BRANDS = {"canon", "sony", "fuji"}
VALID_MODELS = {
    "EOS 200D II": "canon",
    "EOS M50 Mark II": "canon",
    "EOS R50 Mark II": "canon",
    "EOS R6": "canon",
    "PowerShot G7X Mark III": "canon",
    "gfx100ii": "fuji",
    "x-e4": "fuji",
    "x-s20": "fuji",
    "x-t5": "fuji",
    "x100v": "fuji",
    "ILCE-6400 a6400": "sony",
    "ILCE-7M3 a7III": "sony",
    "DSC-RX100M7": "sony",
    "ZV-1": "sony",
    "ZV-E10": "sony",
}


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
    writer(
        {
            "currentNode": "check_validation_criteria(확인을 위한 출력)",
            "answer": "",
            "keywords": [],
            "suggestQuestions": [],
            "sessionId": state.get("sessionId"),
            "messageId": state.get("messageId"),
        }
    )


    completion = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                            "You are an expert in analyzing user questions for a camera manual-based RAG system. "
                            "Your primary task is to process a given user query and extract structured information based on predefined rules.\n\n"
                            "### Input Elements:\n"
                            "- **question**: The user's input question.\n"
                            "- **brand** (optional): The provided camera brand.\n"
                            "- **model** (optional): The provided camera model.\n\n"
                            "### Rules for Extraction:\n"
                            "1. If the **brand** and **model** are explicitly mentioned in the question, extract them.\n"
                            "2. The system supports **only three camera brands** for document retrieval: canon, sony, fuji.\n"
                            "3. Each brand has a predefined set of supported models:\n"
                            f"{VALID_MODELS}\n\n"
                            "4. If the extracted **brand** and **model** are not in the predefined list, return `null` for each.\n\n"
                            "### Brand Normalization:\n"
                            "To ensure consistent brand extraction, convert brand names to match `VALID_BRANDS`. "
                            "This includes handling variations in spelling, capitalization, and language (Korean/English).\n"
                            "- Canon (캐논, 캐논카메라, CANON, canon) → `canon`\n"
                            "- Sony (소니, SONY, sony) → `sony`\n"
                            "- Fujifilm (후지, 후지필름, FUJIFILM, fuji) → `fuji`\n"
                            "If the brand name does not match the above mappings, return `null`.\n\n"
                            "### Intent Analysis:\n"
                            "You must determine the user's intent by classifying the question into two categories:\n"
                            "- `is_camera_related`: **true** if the question is related to cameras, **false** otherwise.\n"
                            "- `is_manual_related`: **true** if the question pertains to settings/configurations that can be found in a camera manual, **false** otherwise.\n\n"
                            "### Output Format:\n"
                            "Return the result in JSON format:\n"
                            "{\n"
                            '  "brand": "Extracted brand or null",\n'
                            '  "model": "Extracted model or null",\n'
                            '  "is_camera_related": true/false,\n'
                            '  "is_manual_related": true/false\n'
                            "}\n\n"
                            "### Final Note:\n"
                            "- Do **not** modify, interpret, or add explanations to the extracted data.\n"
                            "- Follow the given brand and model constraints strictly."
                        )
            },
            {
                "role": "user",
                "content": f'''
"question": {state["question"]}
"brand": {state.get('brand', None)}
"model": {state.get('model', None)}
'''
            }
        ],
        response_format=CameraQuestionAnalysis,
    )

    question_analysis = completion.choices[0].message.parsed

    model = None
    brand = None
    if question_analysis.model:
        model = question_analysis.model
    if question_analysis.brand:
        brand = question_analysis.brand

    validation_results = {
           "camera_question": question_analysis.is_camera_related,
            "is_setting": question_analysis.is_manual_related,
            "choose_brand": True if question_analysis.brand else False,
            "choose_model": True if question_analysis.model else False             
    }

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
        elif (not validation_results["choose_brand"]) or (not validation_results["choose_model"]):
            next_step = "ask_brand" # 역질문 노드
        elif not validation_results["is_setting"]:
            next_step = "settings_generate" # 사용자 메뉴얼 관련 답변 및 질문 재생성 노드
    
    return {
        "model": model,
        "brand": brand,
        "validation_results":{
                                "camera_question": question_analysis.is_camera_related,
                                "is_setting": question_analysis.is_manual_related,
                                "choose_brand": True if question_analysis.brand else False,
                                "choose_model": True if question_analysis.model else False
                            },
        "next_step": next_step

    }






















# def parse_validation_results(text: str) -> Dict[str, bool]:
#     """ LLM 응답을 리스트로 변환 후 Dict로 매핑 """
#     try:
#         parsed_json = json.loads(text)  # JSON 형식이면 바로 변환
#     except:
#         parsed_json = list(filter(None, text.replace("[","").replace("]","").strip().split(",")))  # 개행 문자 기준으로 분리 후 빈 값 제거

#     return {
#         "camera_question": True,
#         "is_setting": True,
#         "choose_brand": None
#     }
#     # return {
#     #     "camera_question": parsed_json[0] == "TRUE",
#     #     "is_setting": parsed_json[1] == "TRUE",
#     #     "choose_brand": parsed_json[2] == "TRUE"
#     # }

# parse_lambda = RunnableLambda(parse_validation_results)  # LCEL에서 Lambda로 실행

# def check_validation_criteria(state: InputState, writer: StreamWriter) -> RouterState:
#     writer(
#         {
#             "currentNode": "질문 분석 중",
#             "answer": "",
#             "keywords": [],
#             "suggestQuestions": [],
#             "sessionId": state.get("sessionId"),
#             "messageId": state.get("messageId"),
#         }
#     )
#     question = state['question']
#     brand = state.get('brand', None)  # 선택적 필드는 `.get()` 사용
#     model = state.get('model', None)  # 선택적 필드
#     llm = ChatOpenAI(temperature=0, model="gpt-4o")
    
#     # 검증 템플릿
#     validation_prompt = ChatPromptTemplate.from_template("""
#     다음은 사용자의 질문과 선택한 브랜드 및 모델 정보입니다. 이를 바탕으로 세 가지 사항을 판단하세요. 각 판단은 TRUE 또는 FALSE로 리스트 형태로 반환합니다.

#     1. 사용자의 질문이 카메라와 관련된 질문인지 판단하세요. (카메라 기기, 기능, 설정, 사용법 등과 관련된 질문이면 TRUE, 아니면 FALSE)
#     2. 브랜드 정보를 판단하세요.  
#     - 선택한 브랜드가 None이 아니라면 TRUE  
#     - 브랜드가 None이지만 질문 내에 브랜드가 언급되어 있다면 TRUE  
#     - 위 두 조건에 해당하지 않으면 FALSE  
#     3. 모델 정보를 판단하세요.  
#     - 선택한 모델이 None이 아니라면 TRUE  
#     - 모델이 None이지만 질문 내에 모델이 언급되어 있다면 TRUE  
#     - 위 두 조건에 해당하지 않으면 FALSE  

#     사용자 질문: {question}  
#     선택한 브랜드: {brand}  
#     선택한 모델: {model}  

#     판단 결과를 [TRUE, TRUE, FALSE] 형식으로 반환하세요.
#     """)

#     # LCEL 기반 실행 체인
#     llm_chain = (
#         validation_prompt| llm | StrOutputParser() | parse_lambda  # Dict[str, bool] 형태로 변환
#     )
    
#     # 검증 실행
#     validation_results = llm_chain.invoke({"question": question, "brand": brand, "model": model})
#     return {
#         **state,
#         "validation_results": validation_results
#     }
    