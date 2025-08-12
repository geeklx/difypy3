from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from typing import Generator
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# 从环境变量中读取数据库连接配置
DB_USER = 'root'
DB_PASSWORD = '123456'
DB_HOST = 'localhost'
DB_HOST2 = 'g25.geekaiapp.icu'
DB_PORT = '3306'
DB_NAME = 'student_score'
# DB_NAME = 'os.getenv("DB_NAME")'

# 构建数据库URL     mysql+mysqlconnector://root:123456@192.168.31.115:3306/student_score
# 构建数据库URL     mysql+mysqlconnector://root:123456@192.168.31.115:3306/test_db
# 构建数据库URL     mysql+pymysql://root:123456%40192.168.31.115:3306/student_score
# 构建数据库URL     mysql+pymysql://root:123456%40192.168.31.115:3306/test_db
# 构建数据库URL     mysql+pymysql://root:123456@192.168.31.115:3306/test_db
# 构建数据库URL     mysql+pymysql://root:123456@localhost:3306/test_db
DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST2}/{DB_NAME}"

# 创建数据库引擎
engine = create_engine(DATABASE_URL)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 获取数据库会话
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()