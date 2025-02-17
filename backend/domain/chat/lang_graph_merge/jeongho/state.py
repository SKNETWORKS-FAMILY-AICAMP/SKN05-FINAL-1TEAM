from typing_extensions import TypedDict, Annotated, Optional
from pydantic import BaseModel, Field
from langgraph.graph.message import add_messages

class subOverallState(TypedDict):
    question: Annotated[str, "Question"]
    ex_question: Annotated[str, "issettingbeforequstion"]
    brand: Annotated[Optional[str],"brandname"]
    model: Annotated[Optional[str],"modelname"]
    context: Annotated[list, "Context"]
    message: Annotated[list, add_messages]
    answer: Annotated[str, "Answer"]
    keyword: Annotated[list, "keywordExtract"]
    suggest_question: Annotated[list, "suggestquestion"]
    sessionId: Annotated[int, "SessionID"]
    messageId: Annotated[int, "MessageID"]

class InputState(BaseModel):
    sessionId: Annotated[int, "SessionID"]
    messageId: Annotated[int, "MessageID"]
    brand: Optional[str] = Field(default=None)
    model: Optional[str] = Field(default=None)
    question: str  # question은 반드시 있어야 하므로 Optional 아님

class RetrievalState(TypedDict):
    model: str
    query: str
    query_decompose: list[str]
    multi_query_expansion: list[list[str]]
    hybrid_cc_IDs: list[list[list[str]]]
    rerank_passages: list[list[list[str]]]
    rerank_passages_metadata: list[list[list[dict]]]
    sessionId: Annotated[int, "SessionID"]
    messageId: Annotated[int, "MessageID"]

class GenerateState(TypedDict):
    query: str
    context: Annotated[list, "Context"]
    answers: list[str]
    answer: str
    sessionId: Annotated[int, "SessionID"]
    messageId: Annotated[int, "MessageID"]

class OutputState(BaseModel):
    temp: str
    currentNode: str
    sessionId: Annotated[int, "SessionID"]
    messageId: Annotated[int, "MessageID"]
    answer: str
    keywords: list
    suggestQuestions: list