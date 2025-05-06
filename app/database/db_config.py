# app/database/db_config.py
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 获取数据库URL，如果环境变量不存在则使用默认值
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:abc123@localhost:3306/smartqa_db")

# 创建数据库引擎
engine = create_engine(DATABASE_URL)

# 创建会话类
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基类
Base = declarative_base()

# 获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()