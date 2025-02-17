from typing import Optional, Dict
from typing_extensions import TypedDict, Annotated
from langgraph.graph.message import add_messages


class RequiredInputState(TypedDict):
    question: str  # 필수 필드
    sessionId: Annotated[int, "SessionID"]
    messageId: Annotated[int, "MessageID"]

class OptionalInputState(TypedDict, total=False):
    brand: Annotated[Optional[str], "brandname"]  # 선택적 필드
    model: Annotated[Optional[str], "modelname"]  # 선택적 필드

class InputState(RequiredInputState, OptionalInputState):
    """ 필수 필드와 선택적 필드를 분리하여 `question`만 필수로 유지 """

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
    context: Annotated[list, "Context"]
    message: Annotated[list, add_messages]
    answer: Annotated[str, "Answer"]
    keyword: Annotated[list, "keywordExtract"]
    suggest_question: Annotated[list, "suggestquestion"]
    validation_results: dict
    sessionId: Annotated[int, "SessionID"]
    messageId: Annotated[int, "MessageID"]
    next_step: Annotated[str, "routerstep"]
    relevance: Annotated[str, "relevance"]

# hidden state
class RouterState(TypedDict):
    question: Annotated[str, "Question"]
    brand: Annotated[Optional[str],"brandname"]
    model: Annotated[Optional[str],"modelname"]
    next_step: Annotated[str, "routerstep"]
    validation_results: Optional[Dict[str, bool]]
    new_queries: list
    awaiting_user_input: Annotated[bool, "사용자 입력 대기 상태"]
    question_context: Annotated[Dict, "질문 컨텍스트 저장"]  # 새로 추가
    sessionId: Annotated[int, "SessionID"]
    messageId: Annotated[int, "MessageID"]