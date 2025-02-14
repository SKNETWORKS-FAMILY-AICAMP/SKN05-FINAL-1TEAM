from langgraph.errors import GraphInterrupt
from langgraph.types import interrupt
from langgraph.types import StreamWriter
from domain.chat.lang_graph_merge.state import RouterState
from pydantic import BaseModel
from typing import Optional
from openai import OpenAI


client = OpenAI()

# 📌 Pydantic 데이터 모델 정의
class UserQueryAnalysis(BaseModel):
    brand: Optional[str]  # 추출된 브랜드 (없으면 None)
    model: Optional[str]  # 추출된 모델 (없으면 None)
    newquestion: Optional[str]  # 새로운 질문이 들어온 경우 (없으면 None)
    reject_input: bool  # 사용자가 브랜드/모델 입력을 거부했는지 여부

# 📌 지원되는 브랜드 및 모델 목록
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


def refine_question(state: RouterState, writer: StreamWriter) -> RouterState:

    writer(
        {
            "currentNode": "refine_question(확인을 위한 출력)",
            "answer": "",
            "keywords": [],
            "suggestQuestions": [],
            "sessionId": state.get("sessionId"),
            "messageId": state.get("messageId"),
        }
    )

    validation_results = state["validation_results"]

    if not state.get("brand") and not state.get("model"):
        new_queries = "알고 싶은 카메라 브랜드와 모델이 있으신가요?"

    if not state.get("model"):
        brand = state.get("brand")

        if brand in {"canon", "fuji", "sony"}:
            # 해당 브랜드의 모델 리스트 가져오기
            model_list = [model for model, b in VALID_MODELS.items() if b == brand]

            # 질문 생성
            new_queries = f"{brand} 브랜드의 카메라 모델 중에서 선택해주세요:\n" + \
                        "\n".join([f"- {model}" for model in model_list]) + \
                        "\n또는 원하지 않으면 '없다'라고 입력해주세요."
        else:
            new_queries = '''알고 싶은 카메라 브랜드가 있으신가요?  
Canon, Fuji, Sony 중 하나를 선택하시거나, 원하지 않으시면 "없다"라고 입력해주세요.'''



    try:
        model_answer = interrupt(new_queries)
    except GraphInterrupt:
        writer(
            {
                "currentNode": "refine_question",
                "answer": new_queries,
                "keywords": [],
                "suggestQuestions": [],
                "sessionId": state.get("sessionId"),
                "messageId": state.get("messageId"),
            }
        )
        raise  # 첫 번째 시도에서 예외 발생 후 종료

    completion = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=[
            {
    "role": "system",
    "content": (
        "You are an expert in analyzing user responses for a camera manual-based RAG system. "
        "Your task is to process user input from a follow-up question where they were asked to provide a brand or model.\n\n"
        "### Input Elements:\n"
        "- **originalquestion**: The user's initial question before requesting a brand/model.\n"
        "- **brand** (optional): The previously provided camera brand.\n"
        "- **model** (optional): The previously provided camera model.\n"
        "- **query**: The user's response regarding the brand or model.\n\n"
        "### Rules for Extraction:\n"
        "- Extract and return the brand if it is valid.\n"
        f"  - VALID_BRANDS: {VALID_BRANDS}\n"
        "- Extract and return the model if it is valid.\n"
        f"  - VALID_MODELS: {VALID_MODELS}\n"
        "- If the response does not contain a valid brand or model but includes a new question, set it under `newquestion`.\n"
        "- If the user explicitly refuses to provide a brand or model (e.g., 'I don't have a preferred brand'),\n"
        "  set `reject_input` to `true` and return `null` for `brand` and `model`.\n\n"
        "### Brand Normalization:\n"
        "Ensure extracted brands match `VALID_BRANDS`. Normalize spelling, capitalization, and language variations:\n"
        "- Canon (캐논, CANON, canon) → `canon`\n"
        "- Sony (소니, SONY, sony) → `sony`\n"
        "- Fujifilm (후지, 후지필름, FUJIFILM, fuji) → `fuji`\n\n"
        "### Intent Recognition:\n"
        "- Compare `originalquestion` and `query`:\n"
        "  1. If the topic remains the same but with a different brand or model, set `newquestion` and reset `brand` and `model`.\n"
        "  2. If the `query` introduces a completely different topic, extract it and return it under `newquestion`.\n"
        "  3. If the `query` is **not related to cameras at all** (e.g., about food, weather, or other non-camera topics), return `null` for `brand`, `model`, and `newquestion`.\n\n"
        "### Output Format:\n"
        "{\n"
        '  "brand": "Extracted brand or null",\n'
        '  "model": "Extracted model or null",\n'
        '  "newquestion": "Extracted new question or null",\n'
        '  "reject_input": true/false\n'
        "}\n\n"
        "### Final Note:\n"
        "- Do **not** modify, interpret, or add explanations to the extracted data.\n"
        "- Follow the given brand and model constraints strictly."
    )
},
{
    "role": "user",
    "content": f'''
User Input:
"originalquestion": {state["question"]}
"brand": {state.get("brand", "No brand information provided")}
"model": {state.get("model", "No model information provided")}
"query": {model_answer}
'''

},
        ],
        response_format=UserQueryAnalysis,
    )

    user_response_analysis = completion.choices[0].message.parsed



    model_name = state.get("model", None)
    brand_name = state.get("brand", None)
    print(f"user_response_analysis: {user_response_analysis}")
    print(f"state: {state}")
    print(f'state.get("model"): {state.get("model")}')
    if not state.get("model", None) and user_response_analysis.model:
        model_name = user_response_analysis.model
    if not state.get("brand", None) and user_response_analysis.brand:
        brand_name = user_response_analysis.brand

    if user_response_analysis.newquestion:
        next_step = "validate_input"
        return {"question": user_response_analysis.newquestion,"brand": None, "model":None, "next_step": next_step}
    elif user_response_analysis.reject_input:
        if brand_name == 'canon':
            return {"brand": brand_name, "model": model_name, "next_step": "rag_canon"}
        elif brand_name == 'sony':
            return {"brand": brand_name, "model": model_name, "next_step": "rag_sony"}
        else:
            return {"brand": "fuji", "model": model_name, "next_step": "rag_fuji"}

    elif (
            not user_response_analysis.brand
            and not user_response_analysis.model
            and not user_response_analysis.newquestion 
            and not user_response_analysis.reject_input
        ):
        next_step = "not_for_camera" 
        return {"question": model_answer, "brand": brand_name, "model": model_name, "next_step": next_step}
    elif not validation_results["is_setting"]:
        next_step = "settings_generate" # 사용자 메뉴얼 관련 답변 및 질문 재생성 노드
        return {"brand": brand_name, "model": model_name, "next_step": next_step}
    
    elif brand_name and model_name:
        if brand_name == 'canon':
            return {"brand": brand_name, "model": model_name, "next_step": "rag_canon"}
        elif brand_name == 'sony':
            return {"brand": brand_name, "model": model_name, "next_step": "rag_sony"}
        elif brand_name == 'fuji':
            return {"brand": brand_name, "model": model_name, "next_step": "rag_fuji"}
    
    elif brand_name and not model_name:
        return {"brand": brand_name, "model": model_name, "next_step": "ask_brand"}

