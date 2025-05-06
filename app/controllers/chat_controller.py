# app/controllers/chat_controller.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.chat_model import (
    ChatRequest, ChatResponse, AIRoleResponse, 
    ConversationCreate, ConversationResponse, 
    MessageResponse, ConversationHistoryResponse
)
from app.services.chat_service import ChatService
from app.database.db_config import get_db
from typing import List
from datetime import datetime

router = APIRouter()
chat_service = ChatService()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """
    处理聊天请求
    """
    try:
        result = chat_service.get_ai_response(
            db=db,
            user_message=request.message,
            conversation_id=request.conversation_id,
            role_id=request.role_id,
            user_id=request.user_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/roles", response_model=List[AIRoleResponse])
async def get_roles(db: Session = Depends(get_db)):
    """
    获取所有AI角色
    """
    try:
        roles = chat_service.get_all_roles(db)
        return [
            AIRoleResponse(
                id=role.id,
                name=role.name,
                description=role.description
            )
            for role in roles
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conversations/{user_id}", response_model=List[ConversationResponse])
async def get_user_conversations(user_id: str, db: Session = Depends(get_db)):
    """
    获取用户的所有对话
    """
    try:
        conversations = chat_service.get_user_conversations(db, user_id)
        return [
            ConversationResponse(
                id=conv.id,
                title=conv.title,
                role_id=conv.role_id,
                role_name=conv.role.name,
                updated_at=conv.updated_at.isoformat()
            )
            for conv in conversations
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conversation/{conversation_id}", response_model=List[MessageResponse])
async def get_conversation_messages(conversation_id: int, db: Session = Depends(get_db)):
    """
    获取对话的所有消息
    """
    try:
        _, messages = chat_service.get_conversation_history(db, conversation_id)
        return [
            MessageResponse(
                role=msg.role,
                content=msg.content,
                created_at=msg.created_at.isoformat()
            )
            for msg in messages
        ]
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/conversation", response_model=ConversationResponse)
async def create_conversation(request: ConversationCreate, db: Session = Depends(get_db)):
    """
    创建新对话
    """
    try:
        # 确保用户存在
        chat_service.get_or_create_user(db, request.user_id)
        
        conversation = chat_service.create_conversation(
            db=db,
            user_id=request.user_id,
            role_id=request.role_id,
            title=request.title
        )
        
        role = chat_service.get_role_by_id(db, conversation.role_id)
        
        return ConversationResponse(
            id=conversation.id,
            title=conversation.title,
            role_id=conversation.role_id,
            role_name=role.name,
            updated_at=conversation.updated_at.isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    return {"status": "healthy"}