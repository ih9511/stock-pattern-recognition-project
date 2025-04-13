"""테이블 생성"""
from backend.app.database import engine, Base
from backend.app import models

Base.metadata.create_all(bind=engine)