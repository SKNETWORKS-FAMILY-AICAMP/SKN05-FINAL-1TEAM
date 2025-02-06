from typing_extensions import TypedDict, Annotated
from typing import Optional, Dict
from langgraph.graph.message import add_messages

class InputState(TypedDict):
    question: str  # 필수 필드
    brand: Annotated[Optional[str], "brandname"]  # 선택적 필드
    model: Annotated[Optional[str], "modelname"]  # 선택적 필드

class OutputState(TypedDict):
    message: Annotated[list, add_messages]
    answer: Annotated[str, "Answer"]
    keyword: Annotated[list, "keywordExtract"]
    suggest_question: Annotated[list, "suggestquestion"]
    
# 전체 state
class OverallState(TypedDict):
    question: Annotated[str, "Question"]
    ex_question: Annotated[str, "issettingbeforequstion"]
    brand: Annotated[Optional[str],"brandname"]
    model: Annotated[Optional[str],"modelname"]
    message: Annotated[list, add_messages]
    context: Annotated[list, "context"]
    answer: Annotated[str, "Answer"]
    keyword: Annotated[list, "keywordExtract"]
    suggest_question: Annotated[list, "suggestquestion"]
    next_step: Annotated[str, "routerstep"]
    validation_results: Dict[str, bool]  
    relevance: Annotated[str, "relevance check"]

# hidden state
class RouterState(TypedDict):
    question: Annotated[str, "Question"]
    brand: Annotated[Optional[str],"brandname"]
    model: Annotated[Optional[str],"modelname"]
    new_queries: list
    awaiting_user_input: Annotated[bool, "사용자 입력 대기 상태"]
    question_context: Annotated[Dict, "질문 컨텍스트 저장"]  # 새로 추가