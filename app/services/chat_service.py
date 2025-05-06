# app/services/chat_service.py
import requests
import logging
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from app.database import crud, models
import uuid

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatService:
    def __init__(self):
        self.api_key = "sk-owciyggqpjmjgqnnhhbganzfayhyhpqnllgefajgoipbuidz"
        self.api_url = "https://api.siliconflow.cn/v1/chat/completions"
        self.model_name = "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B"
    
    def get_ai_response(self, db: Session, user_message: str, conversation_id: Optional[int] = None, role_id: Optional[int] = None, user_id: Optional[str] = None) -> Dict:
        """
        调用硅基流动平台API获取AI回答并保存到数据库
        """
        logger.info(f"收到用户消息: {user_message}")
        
        # 确保用户存在
        if not user_id:
            user_id = str(uuid.uuid4())
        crud.get_or_create_user(db, user_id)
        
        # 处理对话ID
        if not conversation_id:
            if not role_id:
                role_id = 1  # 默认使用"通用助手"角色
            conversation = crud.create_conversation(db, user_id, role_id)
            conversation_id = conversation.id
        else:
            conversation = crud.get_conversation_by_id(db, conversation_id)
            if not conversation:
                raise ValueError(f"对话ID {conversation_id} 不存在")
            role_id = conversation.role_id
        
        # 获取角色系统提示词
        role = crud.get_role_by_id(db, role_id)
        system_prompt = role.system_prompt
        
        # 保存用户消息到数据库
        crud.create_message(db, conversation_id, "user", user_message)
        
        # 准备API请求
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        # 添加历史消息（最多5轮）
        history_messages = crud.get_messages_by_conversation(db, conversation_id)
        if len(history_messages) > 2:  # 如果有历史消息
            history = []
            # 从倒数第3条开始取（因为最后2条是刚刚添加的用户消息和即将添加的AI回复）
            for msg in history_messages[-10:-1]:  # 最多添加最近的5轮对话
                history.append({"role": msg.role, "content": msg.content})
            
            # 在system和user消息之间插入历史消息
            messages = [messages[0]] + history + [messages[1]]
        
        payload = {
            "model": self.model_name,
            "messages": messages,
            "stream": False,
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        logger.info(f"正在调用硅基流动API...")
        response = requests.post(self.api_url, headers=headers, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result['choices'][0]['message']['content']
            logger.info(f"API调用成功，AI回复长度: {len(ai_response)}")
            
            # 保存AI回复到数据库
            crud.create_message(db, conversation_id, "assistant", ai_response)
            
            # 如果是新对话，使用前几个字作为标题
            if conversation.title == "新对话":
                title = user_message[:20] + "..." if len(user_message) > 20 else user_message
                crud.update_conversation_title(db, conversation_id, title)
            
            return {
                "response": ai_response,
                "conversation_id": conversation_id
            }
        else:
            logger.error(f"API调用失败: {response.status_code} - {response.text}")
            raise Exception(f"API调用失败: {response.text}")
    
    def get_all_roles(self, db: Session):
        """获取所有AI角色"""
        return crud.get_all_roles(db)
    
    def get_user_conversations(self, db: Session, user_id: str):
        """获取用户的所有对话"""
        return crud.get_conversations_by_user(db, user_id)
    
    def get_conversation_history(self, db: Session, conversation_id: int):
        """获取完整对话历史"""
        conversation = crud.get_conversation_by_id(db, conversation_id)
        if not conversation:
            raise ValueError(f"对话ID {conversation_id} 不存在")
        
        messages = crud.get_messages_by_conversation(db, conversation_id)
        return conversation, messages
    def get_or_create_user(self, db, user_id):
        return crud.get_or_create_user(db, user_id)
