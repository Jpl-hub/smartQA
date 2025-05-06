# app/database/crud.py
from sqlalchemy.orm import Session
from . import models

# 用户相关操作
def get_or_create_user(db: Session, user_id: str):
    """获取用户，如果不存在则创建"""
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not user:
        user = models.User(user_id=user_id)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

# AI角色相关操作
def get_all_roles(db: Session):
    """获取所有AI角色"""
    return db.query(models.AIRole).all()

def get_role_by_id(db: Session, role_id: int):
    """通过ID获取AI角色"""
    return db.query(models.AIRole).filter(models.AIRole.id == role_id).first()

# 对话相关操作
def create_conversation(db: Session, user_id: str, role_id: int, title: str = "新对话"):
    """创建新对话"""
    conversation = models.Conversation(user_id=user_id, role_id=role_id, title=title)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation

def get_conversations_by_user(db: Session, user_id: str):
    """获取用户的所有对话"""
    return db.query(models.Conversation).filter(models.Conversation.user_id == user_id).order_by(models.Conversation.updated_at.desc()).all()

def get_conversation_by_id(db: Session, conversation_id: int):
    """通过ID获取对话"""
    return db.query(models.Conversation).filter(models.Conversation.id == conversation_id).first()

def update_conversation_title(db: Session, conversation_id: int, title: str):
    """更新对话标题"""
    conversation = get_conversation_by_id(db, conversation_id)
    if conversation:
        conversation.title = title
        db.commit()
        db.refresh(conversation)
    return conversation

# 消息相关操作
def create_message(db: Session, conversation_id: int, role: str, content: str):
    """创建新消息"""
    message = models.Message(conversation_id=conversation_id, role=role, content=content)
    db.add(message)
    db.commit()
    db.refresh(message)
    
    # 更新对话的updated_at字段
    conversation = get_conversation_by_id(db, conversation_id)
    db.commit()
    
    return message

def get_messages_by_conversation(db: Session, conversation_id: int):
    """获取对话的所有消息"""
    return db.query(models.Message).filter(models.Message.conversation_id == conversation_id).order_by(models.Message.created_at).all()