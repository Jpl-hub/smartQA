# app/database/models.py
from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from .db_config import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(36), unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    conversations = relationship("Conversation", back_populates="user")

class AIRole(Base):
    __tablename__ = "ai_roles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    system_prompt = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    conversations = relationship("Conversation", back_populates="role")

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(36), ForeignKey("users.user_id"), nullable=False)
    role_id = Column(Integer, ForeignKey("ai_roles.id"), nullable=False)
    title = Column(String(255), nullable=False, default="新对话")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    user = relationship("User", back_populates="conversations")
    role = relationship("AIRole", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    role = Column(Enum("user", "assistant"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    conversation = relationship("Conversation", back_populates="messages")