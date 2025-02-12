from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()


# 데이터 모델 정의
class UserMessage(BaseModel):
    message_id: str
    content: str
    type: str = "user"

class AIMessage(BaseModel):
    message_id: str
    content: str
    image_path: Optional[str]
    keywords: List[str]
    suggested_questions: List[str]

class ChatSession(BaseModel):
    session_id: str
    user_messages: List[UserMessage]
    ai_messages: List[AIMessage]

sessions = {}

@app.post("/chat")
async def chat_with_ai(session_id: str, message: str):
    """
    사용자 메시지와 세션 ID를 기반으로 AI 응답 생성.
    """
    if session_id not in sessions:
        sessions[session_id] = ChatSession(
            session_id=session_id, user_messages=[], ai_messages=[]
        )

    session = sessions[session_id]
    user_message = UserMessage(message_id="user1", content=message)
    session.user_messages.append(user_message)

    # Mock AI 응답 생성
    ai_message = AIMessage(
        message_id="ai1",
        content=f"AI 응답: {message}",
        image_path="/images/sample.png",
        keywords=["Keyword1", "Keyword2"],
        suggested_questions=["What is AI?", "How does it work?"],
    )
    session.ai_messages.append(ai_message)

    return ai_message
