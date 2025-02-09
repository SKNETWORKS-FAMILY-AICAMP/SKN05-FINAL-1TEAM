from pydantic import BaseModel, Field
from typing_extensions import TypedDict

class InputState(BaseModel):
    sessionId: int = Field(default=None, description="없으면 새로운 session 생성")
    brand: str = Field(default=None)
    model: str = Field(default=None)
    question: str

class RetrievalState(TypedDict):
    model: str
    query: str
    query_decompose: list[str]
    multi_query_expansion: list[list[str]]
    hybrid_cc_IDs: list[list[list[str]]]
    rerank_passages: list[list[list[str]]]
    rerank_passages_metadata: list[list[dict]]

class GenerateState(TypedDict):
    query: str
    answers: list[str]
    answer: str

class OutputState(BaseModel):
    temp: str
    currentNode: str
    sessionId: int
    messageId: int
    answer: str
    keywords: list
    suggestQuestions: list










class OverallState(TypedDict):
    temp: str