import difflib
from langchain_core.runnables import RunnableLambda
from langgraph.types import interrupt
from langgraph.types import StreamWriter
from domain.chat.lang_graph_merge.state import RouterState

# 브랜드 매핑 (한글 → 영어)
BRAND_MAPPING = {
    "캐논": "canon",
    "소니": "sony",
    "후지": "fuji",
    "후지필름": "fuji",
    "Canon": "canon",
    "Sony": "sony",
    "Fuji": "fuji",
    "Fujifilm": "fuji",
}

# 모델-브랜드 매핑 (띄어쓰기가 포함된 모델 지원)
MODEL_BRAND_MAPPING = {
    "EOS 200D II": "canon",
    "EOS M50 Mark II": "canon",
    "EOS R50 Mark II": "canon",
    "EOS R6": "canon",
    "PowerShot G7X Mark III": "canon",
    "GFX100II": "fuji",
    "X-E4": "fuji",
    "X-S20": "fuji",
    "X-T5": "fuji",
    "X100V": "fuji",
    "ILCE-6400 a6400": "sony",
    "ILCE-7M3 a7III": "sony",
    "DSC-RX100M7": "sony",
    "ZV-1": "sony",
    "ZV-E10": "sony",
}

# 지원하는 모델 리스트 (띄어쓰기가 포함된 모델을 인식)
VALID_MODELS = list(MODEL_BRAND_MAPPING.keys())
flag = True

def extract_brand_model(user_input: str):
    """
    사용자의 문장에서 브랜드와 모델을 자동 추출
    - 띄어쓰기가 포함된 모델명을 지원
    - 모델을 먼저 감지 → 해당하는 브랜드 자동 매핑
    """
    user_input = user_input.lower().strip()

    # 모델명 유사도 매칭 (Fuzzy Matching) - 띄어쓰기 포함 모델 탐색
    words = user_input.split()  # 문장을 단어별로 분할

    detected_model = None
    detected_brand = None

    # N-gram 방식으로 연속된 단어 조합 탐색 (2-gram, 3-gram)
    n_grams = []
    for n in range(1, 4):  # 1-gram ~ 3-gram 까지 확인
        for i in range(len(words) - n + 1):
            n_grams.append(" ".join(words[i:i + n]))

    # N-gram을 활용하여 모델명 매칭 시도
    for candidate in n_grams:
        closest_match = difflib.get_close_matches(candidate, VALID_MODELS, n=1, cutoff=0.6)
        if closest_match:
            detected_model = closest_match[0]  # 가장 유사한 모델명 선택
            detected_brand = MODEL_BRAND_MAPPING[detected_model]  # 모델에 맞는 브랜드 자동 선택
            break  # 첫 번째 매칭된 모델 사용

    # 사용자가 브랜드를 입력한 경우, 정규화하여 비교
    for kor_brand, eng_brand in BRAND_MAPPING.items():
        if kor_brand.lower() in user_input:
            if detected_brand and detected_brand != eng_brand:
                print(f" 사용자 입력 브랜드({eng_brand})와 모델({detected_model})의 브랜드({detected_brand})가 다릅니다!")
            detected_brand = eng_brand  # 브랜드 업데이트
            break  # 첫 번째 매칭된 브랜드 사용

    return detected_brand, detected_model



def refine_question(state: RouterState, writer: StreamWriter) -> RouterState:
    """
    사용자의 브랜드/모델 정보가 부족할 경우 보완 질문을 생성
    """
    validation_results = state["validation_results"]
    if not state.get("brand") and not state.get("model"):
        new_queries = "알고 싶은 카메라 브랜드와 모델이 있으신가요?"

    elif not state.get("model"):
        new_queries = "알고 싶은 모델이 있으신가요?"

    elif not state.get("brand"):
        new_queries = "알고 싶은 브랜드가 있으신가요?"
    print(state)
    global flag
    if flag:
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
        flag = False

    while True:
        model_answer = interrupt(new_queries)
        flag = True
        brand_name, model_name = extract_brand_model(model_answer)
        validation_results["choose_brand"] = True
        
        if not validation_results["is_setting"]:
            next_step = "settings_generate" # 사용자 메뉴얼 관련 답변 및 질문 재생성 노드
        else:
            if brand_name == 'canon':
                next_step = "rag_canon" # subgraph
            elif brand_name == 'sony':
                next_step = "rag_sony" # subgraph
            elif brand_name == 'fuji':
                next_step = "rag_fuji" # subgraph

        return {
            **state,
            "brand": brand_name,
            "model": model_name,
            "next_step": next_step
        }

# refine_question_node = RunnableLambda(refine_question)





# async def delay_node(state: GraphState, writer: StreamWriter) -> Dict[str, Any]:
#     time.sleep(3)
#     writer(
#         {
#             "currentNode": "delay_node",
#             "sessionId": state["sessionId"],
#             "messageId": state["messageId"],
#             "answer": "",
#             "keywords": [],
#             "suggestQuestions": []
#         }
#     )