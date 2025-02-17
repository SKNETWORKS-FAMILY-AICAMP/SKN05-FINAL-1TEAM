from sqlalchemy.orm import Session
from models import User, ChatSession, History
from datetime import datetime
from domain.chat import chat_schema

def get_session_list(db: Session, user: User):
    session_list = db.query(ChatSession)\
        .filter(ChatSession.user_id == user.user_id)\
        .order_by(ChatSession.create_date.asc())\
        .all()
    
    session_list = [
        chat_schema.SessionItem(
            session_id=session.session_id,
            title=session.title,
            create_date=session.create_date,
            update_date=session.update_date
        )
        for session in session_list
    ]
    return chat_schema.SessionList(session_list=session_list)

def make_session(db: Session, user_id, title):
    db_session = ChatSession(
        user_id=user_id,
        title=title,
        create_date=datetime.now(),
        update_date=datetime.now()
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session.session_id

def delete_session(db: Session, session_id):
    db_session = db.query(ChatSession).filter(ChatSession.session_id == session_id).first()

    db.delete(db_session)
    db.commit()

def update_session(db: Session, session_id):
        # 데이터베이스에서 해당 세션을 조회
    db_session = db.query(ChatSession).filter(ChatSession.session_id == session_id).first()
    
    if not db_session:
        raise ValueError(f"Session with ID {session_id} not found")

    db_session.update_date = datetime.now()
    db.commit()

def make_messageId(db: Session, session_id):
    db_history = History(session_id=session_id,
                         userMessage="",
                         aiMessage="",
                         keywords=[],
                         suggestQuestions=[])
    db.add(db_history)
    db.commit()
    db.refresh(db_history)
    return db_history.message_id                    

def save_message(db: Session, session_id, userMessage, aiMessage, keywords, suggestQuestions, messageId):
    db_history = db.query(History).filter(History.message_id == messageId).first()
    
    db_history.session_id = session_id
    db_history.userMessage = userMessage
    db_history.aiMessage = aiMessage
    db_history.keywords = keywords
    db_history.suggestQuestions = suggestQuestions

    db.commit()

def delete_message(db: Session, message_id):
    db_history = db.query(History).filter(History.message_id == message_id).first()

    db.delete(db_history)
    db.commit()

def get_message_list(db: Session, session_id: int):
    """
    Get a list of messages for a specific session_id.
    """
    message_list = db.query(History)\
        .filter(History.session_id == session_id)\
        .order_by(History.message_id.asc())\
        .all()

    # Convert SQLAlchemy objects to Pydantic models
    return chat_schema.MessageList(
        Messages=[
            chat_schema.MessageItem(
                message_id=message.message_id,
                userMessage=message.userMessage,
                aiMessage=message.aiMessage,
                keywords=message.keywords,
                suggestQuestions=message.suggestQuestions,
            )
            for message in message_list
        ]
    )


# def create_answer(db: Session, question: Question, answer_create: AnswerCreate):
#     db_answer = Answer(question=question,
#                        content=answer_create.content,
#                        create_date=datetime.now())
#     db.add(db_answer)
#     db.commit()