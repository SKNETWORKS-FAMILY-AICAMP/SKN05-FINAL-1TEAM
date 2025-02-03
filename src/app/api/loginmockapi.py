from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import jwt  # PyJWT 라이브러리 필요
from fastapi import Header

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용 (개발 중에는 이렇게 설정할 수 있지만, 실제 배포 시에는 특정 도메인만 허용하는 것이 좋습니다)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock 데이터베이스
mock_users = [
    {
        "id": "1", 
        "email": "test@d.com", 
        "password": "1234", 
        "username": "Test User"
    }
]

# JWT Secret Key
SECRET_KEY = "your-secret-key"

# 회원가입 요청 데이터 모델
class SignupRequest(BaseModel):
    username: str
    email: str
    password: str

# 회원 데이터 모델
class User(BaseModel):
    username: str
    email: str
    password: str

# 로그인 요청 데이터 모델
class LoginRequest(BaseModel):
    email: str
    password: str

# 회원가입 엔드포인트
@app.post("/api/signup")
async def signup(user: SignupRequest):
    # 중복된 이메일 체크
    if any(u["email"] == user.email for u in mock_users):
        raise HTTPException(status_code=400, detail="이미 존재하는 이메일입니다.")

    # 사용자 데이터를 Mock 데이터베이스에 저장
    new_user = User(
        username=user.username,
        email=user.email,
        password=user.password,
    )
    mock_users.append(new_user.dict())
    return {"status": "success", "message": "회원가입 성공!", "user": new_user}

# 모든 사용자 조회 엔드포인트
@app.get("/api/users")
async def get_users():
    return {"users": mock_users}

# 로그인 엔드포인트
@app.post("/api/login")
async def login(request: LoginRequest):
        # Mock User로 자동 로그인
    mock_user = mock_users[0]
    
    # 실제 요청된 이메일/비밀번호와 상관없이 Mock User의 토큰 생성
    token = jwt.encode(
        {
            "name": mock_user["username"], 
            "email": mock_user["email"]
        }, 
        SECRET_KEY, 
        algorithm="HS256"
    )
    
    return {
        "status": "success", 
        "access_token": token,
        "user": {
            "username": mock_user["username"],
            "email": mock_user["email"]
        }
    }
    # 추후 테스트 완료시 이 내용으로 변경 해야함.
    # for user in mock_users:
    #     if user["email"] == request.email and user["password"] == request.password:
    #         # Access Token 생성
    #         token = jwt.encode({"name": user["username"], "email": user["email"]}, SECRET_KEY, algorithm="HS256")
    #         return {"status": "success", "access_token": token}
    # if not any(user["email"] == request.email for user in mock_users):
    #     raise HTTPException(status_code=404, detail="회원가입 필요")
    # raise HTTPException(status_code=401, detail="잘못된 이메일 또는 비밀번호입니다.")

# 토큰 검증을 위한 엔드포인트
@app.get("/api/verify-token")
async def verify_token(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token")
    
    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return {"valid": True, "user": payload}
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# 현재 사용자 정보 조회 엔드포인트
@app.get("/api/me")
async def get_current_user(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token")
    
    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user = next((u for u in mock_users if u["email"] == payload["email"]), None)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return {
            "username": user["username"],
            "email": user["email"]
        }
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")