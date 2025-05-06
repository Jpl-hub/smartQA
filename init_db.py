# 创建一个脚本 init_db.py
from app.database.db_config import engine, get_db
from app.database import models
from app.database.models import AIRole
from sqlalchemy.orm import Session

# 创建表
models.Base.metadata.create_all(bind=engine)

# 插入初始数据
db = Session(engine)

# 检查是否已有角色数据
existing_roles = db.query(AIRole).all()
if not existing_roles:
    # 插入初始角色
    roles = [
        AIRole(name="通用助手", description="一个全能型AI助手，可以回答各类问题。", 
              system_prompt="你是一个乐于助人的AI助手，擅长回答各种问题。"),
        AIRole(name="程序员助手", description="帮助你解决编程问题，提供代码示例和建议。", 
              system_prompt="你是一个编程专家，擅长帮助用户解决各种编程问题，提供清晰的代码示例和技术建议。"),
        AIRole(name="学习导师", description="帮助你学习各种知识，解答学术问题。", 
              system_prompt="你是一个耐心的学习导师，擅长解释复杂概念，回答学术问题，并提供学习建议。"),
        AIRole(name="心理咨询师", description="提供心理支持和建议，帮助你处理情绪和压力。", 
              system_prompt="你是一个善解人意的心理咨询师，擅长倾听，提供情感支持，帮助用户处理压力和情绪问题。")
    ]
    db.add_all(roles)
    db.commit()

db.close()