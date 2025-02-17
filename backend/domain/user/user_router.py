from datetime import timedelta, datetime

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt

from database import get_db
from domain.user import user_crud, user_schema
from domain.user.user_crud import pwd_context

from models import User
from domain.user.auth_utils import get_current_user

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
SECRET_KEY = "4ab2fce7a6bd79e1c014396315ed322dd6edb1c5d975c6b74a2904135172c03c"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")

router = APIRouter(
    prefix="/api/user",
)

@router.post("/create", status_code=status.HTTP_200_OK)
def user_create(_user_create: user_schema.UserCreate, db: Session = Depends(get_db)):
    """
    - Pydantic Validation 통과 후에만 이 함수가 호출됨
    - 여기서 사용자 중복 여부, DB 저장 등을 처리
    """
    # (1) 사용자명/이메일 중복 체크
    user = user_crud.get_existing_user(db, user_create=_user_create)
    if user:
        # 사용자명 또는 이메일이 이미 존재하면 해당 메시지 반환
        return {"message": "이미 가입된 사용자입니다."}

    # (2) DB에 새 사용자 생성
    user_crud.create_user(db=db, user_create=_user_create)
    
    # (3) 가입 성공 메시지
    return {"message": "가입성공"}

@router.delete("/delete", status_code=status.HTTP_200_OK)
def user_delete(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_crud.delete_user(db=db, user=current_user)
    return {"message": "탈퇴성공"}

@router.post("/login", response_model=user_schema.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                           db: Session = Depends(get_db)):

    # check user and password
    user = user_crud.get_user(db, form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # make access token
    data = {
        "sub": user.email,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "userId": user.user_id,
        "username": user.username,
        "email": user.email,
        "access_token": access_token,
        "token_type": "bearer",
    }

