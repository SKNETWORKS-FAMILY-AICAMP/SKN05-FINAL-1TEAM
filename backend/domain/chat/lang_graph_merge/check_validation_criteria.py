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


def decide_next_step(state: RouterState, writer: StreamWriter) -> RouterState:
    return {"next_step": state.get("next_step", None)}