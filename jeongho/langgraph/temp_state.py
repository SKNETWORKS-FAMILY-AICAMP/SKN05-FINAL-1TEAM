from typing_extensions import TypedDict, Annotated
from typing import Optional, Dict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

class RequiredInputState(TypedDict):
    question: str  # 필수 필드

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
    brand: Annotated[Optional[str],"brandname"] = None # 브랜드 값 없이 들어올 수 있음.
    model: Annotated[Optional[str],"modelname"] = None # 모델 값 없이 들어올 수 있음.
    # context: Annotated[str, "Context"]
    message: Annotated[list, add_messages]
    answer: Annotated[str, "Answer"]
    keyword: Annotated[list, "keywordExtract"]
    suggest_question: Annotated[list, "suggestquestion"]

# hidden state
class RouterState(TypedDict):
    question: str
    brand: Annotated[Optional[str],"brandname"] = None # 브랜드 값 없이 들어올 수 있음.
    model: Annotated[Optional[str],"modelname"] = None # 모델 값 없이 들어올 수 있음.
    next_step: Annotated[str, "routerstep"]
    validation_results: Dict[str, bool] 
    brand: str
    answer: str