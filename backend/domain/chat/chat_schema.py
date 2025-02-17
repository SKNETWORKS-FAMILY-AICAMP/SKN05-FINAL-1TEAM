from pydantic import BaseModel, Field
from typing import List
import datetime

class SessionItem(BaseModel):
    session_id: int
    title: str
    create_date: datetime.datetime
    update_date: datetime.datetime

class SessionList(BaseModel):
    session_list: List[SessionItem]

class ChatInput(BaseModel):
    session_id: int = Field(default=None, description="없으면 새로운 session_id 생성")
    brand: str = Field(default=None)
    model: str = Field(default=None)
    question: str

class ChatOutput(BaseModel):
    session_id: int
    message_id: str
    current_node: str
    answer: str
    suggest_questions: list
    keywords: list

class MessageItem(BaseModel):
    message_id: int
    userMessage: str
    aiMessage: str
    keywords: list
    suggestQuestions: list

class MessageList(BaseModel):
    Messages: List[MessageItem]

class KeywordExplainOutput(BaseModel):
    description: str