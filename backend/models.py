from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from sqlalchemy.dialects.sqlite import JSON
from database import Base

class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

class ChatSession(Base):
    __tablename__ = "session"

    session_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    title = Column(String)
    create_date = Column(DateTime, nullable=False)
    update_date = Column(DateTime, nullable=False)

class History(Base):
    __tablename__ = "history"

    message_id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("session.session_id"))
    userMessage = Column(String)
    aiMessage = Column(String)
    keywords = Column(JSON)
    suggestQuestions = Column(JSON)