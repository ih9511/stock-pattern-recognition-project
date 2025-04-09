"""테이블 생성"""
from app.database import engine, Base
from app import models

Base.metadata.create_all(bind=engine)