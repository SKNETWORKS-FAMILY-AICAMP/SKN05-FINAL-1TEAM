
from fastapi import HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session
from starlette import status
from fastapi.security import  OAuth2PasswordBearer
from jose import jwt, JWTError

from database import get_db
from domain.user import user_crud

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
SECRET_KEY = "4ab2fce7a6bd79e1c014396315ed322dd6edb1c5d975c6b74a2904135172c03c"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")

def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    else:
        user = user_crud.get_user(db, email=email)
        if user is None:
            raise credentials_exception
        return user