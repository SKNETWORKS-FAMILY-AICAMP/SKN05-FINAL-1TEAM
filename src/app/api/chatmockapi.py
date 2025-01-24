from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid
import jwt

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

def verify_token(authorization: str) -> dict: # 토큰 검증 함수
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token")
    
    token = authorization.split(" ")[1]
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

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
    request: CreateMessageRequest,
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
    
    if session["userId"] != user["email"]:
        raise HTTPException(status_code=403, detail="Unauthorized access")
    
    # Mock AI 응답 생성
    new_message = Message(
        messageId=str(uuid.uuid4()),
        userMessage=request.userMessage,
        aiMessage="이것은 AI의 mock 응답입니다.",
        keywords=["키워드1", "키워드2"],
        suggestedQuestions=["추천 질문 1?", "추천 질문 2?"],
        createdAt=datetime.now().isoformat()
    )
    
    # 세션에 메시지 추가
    session["messages"].append(new_message.dict())
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