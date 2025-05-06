# app/models/chat_model.py
from pydantic import BaseModel
from typing import List, Optional, Dict

# 基本请求/响应模型
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None
    role_id: Optional[int] = None
    user_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: int

# AI角色模型
class AIRoleResponse(BaseModel):
    id: int
    name: str
    description: str

# 对话模型
class ConversationCreate(BaseModel):
    user_id: str
    role_id: int
    title: Optional[str] = "新对话"

class ConversationResponse(BaseModel):
    id: int
    title: str
    role_id: int
    role_name: str
    updated_at: str

# 消息模型
class MessageResponse(BaseModel):
    role: str
    content: str
    created_at: str

# 完整对话历史模型
class ConversationHistoryResponse(BaseModel):
    id: int
    title: str
    role: AIRoleResponse
    messages: List[MessageResponse]