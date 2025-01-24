from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from database import db
import jwt
from datetime import datetime, timedelta
from typing import Optional, List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React 개발 서버 주소
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# JWT 설정
SECRET_KEY = "your-secret-key"  # 실제로는 환경변수로 관리
ALGORITHM = "HS256"

class UserSignup(BaseModel):
    username: str
    password1: str
    password2: str
    email: str

class UserLogin(BaseModel):
    email: str
    password: str

class AnswerRequest(BaseModel):
    brand: Optional[str] = None
    model: Optional[str] = None
    question: str
    userId: int
    sessionId: Optional[int] = None

@app.post("/api/user/create")
async def signup(user_data: UserSignup):
    if not all([user_data.username, user_data.password1, user_data.password2, user_data.email]):
        raise HTTPException(status_code=400, detail="빈 값은 허용하지 않습니다.")
    
    if user_data.password1 != user_data.password2:
        raise HTTPException(status_code=400, detail="비밀번호가 일치하지 않습니다.")
    
    result = db.create_user(user_data.username, user_data.email, user_data.password1)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    
    return {"message": result["message"]}

@app.post("/api/user/login")
async def login(login_data: UserLogin):
    result = db.verify_user(login_data.email, login_data.password)
    
    if not result["success"]:
        raise HTTPException(status_code=401, detail=result["message"])
    
    # JWT 토큰 생성
    token_data = {
        "sub": str(result["userId"]),
        "email": result["email"],
        "exp": datetime.utcnow() + timedelta(days=1)
    }
    access_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    
    return {
        "userId": result["userId"],
        "username": result["username"],
        "access_token": access_token,
        "token_type": "JWT"
    }

@app.get("/api/chat/sessionlist")
async def get_session_list(userId: int = Query(...)):
    user = db.get_user_by_id(userId)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    
    # 세션이 없을 경우에만 더미 세션 생성
    sessions = db.get_user_sessions(userId)
    if not sessions:
        db.create_dummy_session(userId)
        sessions = db.get_user_sessions(userId)
    
    return {
        "session_list": sessions
    }

@app.get("/api/chat/history")
async def get_chat_history(userId: int = Query(...), sessionId: int = Query(...)):
    user = db.get_user_by_id(userId)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    
    user_sessions = db.get_user_sessions(userId)
    session_exists = any(session["sessionId"] == sessionId for session in user_sessions)
    if not session_exists:
        raise HTTPException(status_code=404, detail="세션을 찾을 수 없습니다.")
    
    messages = db.get_chat_history(sessionId)
    return {
        "Messages": messages
    }

@app.post("/api/chat/answer")
async def generate_answer(request: AnswerRequest):
    user = db.get_user_by_id(request.userId)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    
    session_id = request.sessionId
    if session_id is not None:
        user_sessions = db.get_user_sessions(request.userId)
        session_exists = any(session["sessionId"] == session_id for session in user_sessions)
        if not session_exists:
            raise HTTPException(status_code=404, detail="세션을 찾을 수 없습니다.")
    else:
        title = f"대화 {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        session_id = db.create_new_session(request.userId, title)
    
    llm_response = db.mock_llm_response(
        question=request.question,
        brand=request.brand,
        model=request.model
    )
    
    message_id = db.create_message(session_id, request.question, llm_response)
    
    return {
        "currentNode": llm_response["currentNode"],
        "sessionId": session_id,
        "messageId": message_id,
        "answer": llm_response["answer"],
        "keywords": llm_response["keywords"],
        "suggestQuestions": llm_response["suggestQuestions"]
    }

@app.get("/api/chat/keyword")
async def get_keyword_description(keyword: str = Query(...)):
    description = db.keywords_db.get(keyword)
    if not description:
        raise HTTPException(status_code=404, detail="키워드 설명을 찾을 수 없습니다.")
    
    return {
        "description": description
    }