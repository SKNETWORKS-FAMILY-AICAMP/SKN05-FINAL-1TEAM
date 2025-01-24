from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid
import jwt
import asyncio

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# JWT Secret Key (loginmockapi.py와 동일한 키 사용)
SECRET_KEY = "your-secret-key"

# Mock 데이터베이스
mock_sessions = []
mock_messages = []

class Message(BaseModel): # 메시지 타입
    messageId: str
    userMessage: str
    aiMessage: str
    keywords: List[str]
    suggestedQuestions: List[str]
    createdAt: str

class ChatSession(BaseModel): # 채팅 세션 타입
    sessionId: str
    userId: str
    title: str
    messages: List[Message]
    createdAt: str
    updatedAt: str

class CreateSessionRequest(BaseModel): # 세션 생성 요청 타입
    title: str

class CreateMessageRequest(BaseModel): # 메시지 생성 요청 타입
    sessionId: str
    userMessage: str

class MessageRequest(BaseModel):
    sessionId: str
    userMessage: str

def verify_token(authorization: str = None) -> dict:
    if not authorization or not authorization.startswith("Bearer "):
        return {"email": "test@example.com", "username": "Test User"}
    
    try:
        token = authorization.split(" ")[1]
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.InvalidTokenError:
        return {"email": "test@example.com", "username": "Test User"}

# 새로운 세션 생성
@app.post("/api/sessions")
async def create_session(
    request: CreateSessionRequest,
    authorization: str = Header(None)
):
    user = verify_token(authorization)
    
    new_session = {
        "sessionId": str(uuid.uuid4()),
        "userId": user["email"],
        "title": request.title,
        "messages": [],
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat()
    }
    
    mock_sessions.append(new_session)
    return new_session

# 사용자의 모든 세션 조회
@app.get("/api/sessions")
async def get_sessions(authorization: str = Header(None)):
    user = verify_token(authorization)
    
    user_sessions = [
        session for session in mock_sessions 
        if session["userId"] == user["email"]
    ]
    return user_sessions

# 특정 세션 조회
@app.get("/api/sessions/{session_id}")
async def get_session(session_id: str, authorization: str = Header(None)):
    user = verify_token(authorization)
    
    session = next(
        (s for s in mock_sessions if s["sessionId"] == session_id),
        None
    )
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if session["userId"] != user["email"]:
        raise HTTPException(status_code=403, detail="Unauthorized access")
    
    return session

# 세션 제목 업데이트
@app.put("/api/sessions/{session_id}/title")
async def update_session_title(
    session_id: str,
    title: str,
    authorization: str = Header(None)
):
    user = verify_token(authorization)
    
    session = next(
        (s for s in mock_sessions if s["sessionId"] == session_id),
        None
    )
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if session["userId"] != user["email"]:
        raise HTTPException(status_code=403, detail="Unauthorized access")
    
    session["title"] = title
    session["updatedAt"] = datetime.now().isoformat()
    
    return session

# 세션 삭제
@app.delete("/api/sessions/{session_id}")
async def delete_session(session_id: str, authorization: str = Header(None)):
    user = verify_token(authorization)
    
    session_index = next(
        (i for i, s in enumerate(mock_sessions) if s["sessionId"] == session_id),
        None
    )
    
    if session_index is None:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if mock_sessions[session_index]["userId"] != user["email"]:
        raise HTTPException(status_code=403, detail="Unauthorized access")
    
    deleted_session = mock_sessions.pop(session_index)
    return {"message": "Session deleted successfully"}

# 메시지 생성
@app.post("/api/messages")
async def create_message(
    request: MessageRequest,
    authorization: str = Header(None)
):
    user = verify_token(authorization)
    
    # 세션 찾기
    session = next(
        (s for s in mock_sessions if s["sessionId"] == request.sessionId),
        None
    )
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # 임시 지연 추가 (로딩 상태 테스트용)
    await asyncio.sleep(1)
    
    # Mock AI 응답 생성
    new_message = {
        "messageId": str(uuid.uuid4()),
        "userMessage": request.userMessage,
        "aiMessage": f"당신의 질문 '{request.userMessage}'에 대한 답변입니다...",
        "keywords": ["카메라", "설정", "촬영"],  # 실제로는 질문에 따라 다른 키워드 생성
        "suggestedQuestions": [
            "조리개 값은 어떻게 조절하나요?",
            "셔터스피드 설정은 어디서 하나요?",
            "ISO 감도는 어떻게 변경하나요?"
        ],
        "createdAt": datetime.now().isoformat()
    }
    
    session["messages"].append(new_message)
    session["updatedAt"] = datetime.now().isoformat()
    
    return new_message

# 세션의 모든 메시지 조회
@app.get("/api/sessions/{session_id}/messages")
async def get_messages(session_id: str, authorization: str = Header(None)):
    user = verify_token(authorization)
    
    session = next(
        (s for s in mock_sessions if s["sessionId"] == session_id),
        None
    )
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if session["userId"] != user["email"]:
        raise HTTPException(status_code=403, detail="Unauthorized access")
    
    return session["messages"] 