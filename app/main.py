# app/main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.controllers.chat_controller import router as chat_router
from app.database.db_config import engine, get_db
from app.database import models
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 创建表（如果不存在）
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="智能问答系统API")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(chat_router)

# 添加根路径响应
@app.get("/")
async def root():
    return {
        "message": "欢迎使用智能问答系统API",
        "endpoints": {
            "/chat": "POST - 发送聊天消息",
            "/roles": "GET - 获取所有AI角色",
            "/conversations/{user_id}": "GET - 获取用户的所有对话",
            "/conversation/{conversation_id}": "GET - 获取对话的所有消息",
            "/conversation": "POST - 创建新对话",
            "/health": "GET - 健康检查",
            "/docs": "GET - API文档 (Swagger UI)",
            "/redoc": "GET - API文档 (ReDoc)"
        }
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)