import json
from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from starlette import status
from database import get_db
from models import User
from langgraph.types import Command
from domain.user.auth_utils import get_current_user
from domain.chat import chat_schema, chat_crud
from domain.chat.lang_graph_merge.graph import app
from domain.chat.keyword_search import explain_term


router = APIRouter(
    prefix="/api/chat",
)

@router.get("/sessionlist", response_model=chat_schema.SessionList)
def session_list(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    _session_list = chat_crud.get_session_list(db, current_user)
    return _session_list

@router.delete("/sessiondelete", status_code=status.HTTP_200_OK)
def session_delete(session_id: int = Query(..., description="Session ID to filter messages"), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    chat_crud.delete_session(db=db, session_id=session_id)
    return {"message": "삭제성공"}


@router.post("/answer", response_model=list[chat_schema.ChatOutput])
def answer(_chat_input: chat_schema.ChatInput, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not _chat_input.session_id:
        _chat_input.session_id = chat_crud.make_session(db,
                               current_user.user_id,
                               title=_chat_input.question)
    else:
        chat_crud.update_session(db, _chat_input.session_id)

    messageId = chat_crud.make_messageId(db, _chat_input.session_id)
    thread = {"configurable": {"thread_id": _chat_input.session_id}}
    async def event_stream():
        accumulated_data = ""
        keywords = []
        suggestQuestions = []
        try:
            async for chunk in app.astream(
                input={
                    "question": _chat_input.question,
                    "sessionId": _chat_input.session_id, 
                    "messageId": messageId,
                    "brand": _chat_input.brand,
                    "model": _chat_input.model,
                    },
                config=thread,
                stream_mode=["custom"]
            ):
                should_save_message = True
                chunk_data = json.dumps(chunk[1])
                accumulated_data += chunk[1]["answer"]

                if chunk[1]["keywords"]:
                    keywords = chunk[1]["keywords"]
                if chunk[1]["suggestQuestions"]:
                    suggestQuestions = chunk[1]["suggestQuestions"]

                yield chunk_data + "\n"
        except Exception as e:
            pass
        finally:
            chat_crud.save_message(
                db=db,
                session_id=_chat_input.session_id,
                userMessage=_chat_input.question,
                aiMessage=accumulated_data,
                keywords=keywords,
                suggestQuestions=suggestQuestions,
                messageId=messageId
            )

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@router.post("/rqanswer", response_model=list[chat_schema.ChatOutput])
def answer(_chat_input: chat_schema.ChatInput, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not _chat_input.session_id:
        _chat_input.session_id = chat_crud.make_session(db,
                               current_user.user_id,
                               title=_chat_input.question)
    else:
        chat_crud.update_session(db, _chat_input.session_id)

    messageId = chat_crud.make_messageId(db, _chat_input.session_id)
    thread = {"configurable": {"thread_id": _chat_input.session_id}}
    async def event_stream():
        accumulated_data = ""
        keywords = []
        suggestQuestions = []
        try:
            async for chunk in app.astream(
                Command(resume=_chat_input.question),
                config=thread,
                stream_mode=["custom"]
            ):
                should_save_message = True
                chunk_data = json.dumps(chunk[1])
                accumulated_data += chunk[1]["answer"]

                if chunk[1]["keywords"]:
                    keywords = chunk[1]["keywords"]
                if chunk[1]["suggestQuestions"]:
                    suggestQuestions = chunk[1]["suggestQuestions"]

                yield chunk_data + "\n"
        except Exception as e:
            pass
        finally:
            chat_crud.save_message(
                db=db,
                session_id=_chat_input.session_id,
                userMessage=_chat_input.question,
                aiMessage=accumulated_data,
                keywords=keywords,
                suggestQuestions=suggestQuestions,
                messageId=messageId
            )

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@router.get("/history", response_model=chat_schema.MessageList)
def message_list(
    session_id: int = Query(..., description="Session ID to filter messages"),  # 쿼리 파라미터
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    _message_list = chat_crud.get_message_list(db, session_id)
    return _message_list

@router.delete("/historydelete", status_code=status.HTTP_200_OK)
def message_delete(
    message_id: int = Query(...),  # 쿼리 파라미터
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    chat_crud.delete_message(db=db, message_id=message_id)
    return {"message": "삭제성공"}


@router.get("/keyword", response_model=chat_schema.KeywordExplainOutput)
def keyword_explain(
    keyword: str = Query(..., ),  # 쿼리 파라미터
    db: Session = Depends(get_db),
):
    return {"description": f"{explain_term(keyword)}"}