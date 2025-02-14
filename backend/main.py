from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from domain.user import user_router
from domain.chat import chat_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용. 필요한 경우 특정 도메인으로 제한.
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용 (GET, POST, OPTIONS 등)
    allow_headers=["*"],  # 모든 헤더 허용
)

@app.exception_handler(RequestValidationError)
async def user_create_validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    # Pydantic 검증 에러가 발생했을 때의 처리
    errors = exc.errors()
    for err in errors:
        msg = err.get("msg", "")
        if "비밀번호가 일치하지 않습니다" in msg:
            return JSONResponse(status_code=400, content={"message": "비밀번호 불일치"})
        elif "빈 값은 허용되지 않습니다" in msg:
            return JSONResponse(status_code=400, content={"message": "빈 값은 허용되지 않습니다."})
        elif "value is not a valid email address" in msg:
            return JSONResponse(status_code=400, content={"message": "이메일 형식이 일치하지 않습니다."})

    # 그 외 기본 처리는 422
    return JSONResponse(status_code=422, content={"message": "요청 값이 올바르지 않습니다."})


@app.get("/")
def check_api_server():
    return {"message": "api서버 켜져있음"}

app.include_router(user_router.router)
app.include_router(chat_router.router)