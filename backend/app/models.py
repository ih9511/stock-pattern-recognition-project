"""SQLAlchemy 모델 정의"""
from sqlalchemy import Column, String, Date, Float, BigInteger, Boolean
from .database import Base

class StockPrice(Base):
    __tablename__ = "stock_prices"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    symbol = Column(String(10), nullable=False)
    date = Column(String(10), nullable=False)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(BigInteger)

class StockMeta(Base):
    __tablename__ = "stock_meta"

    symbol = Column(String(10), primary_key=True)
    name = Column(String(100))
    sector = Column(String(100))
    industry = Column(String(100))
    exchange = Column(String(10))

class TechnicalIndicator(Base):
    __tablename__ = "technical_indicators"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    symbol = Column(String(10), nullable=False)
    date = Column(Date, nullable=False)
    indicator_name = Column(String(50), nullable=False)
    value = Column(Float)
    
class StockTicker(Base):
    __tablename__ = "stock_tickers"
    
    symbol = Column(String(10), primary_key=True)
    name =  Column(String(100))
    exchange = Column(String(10))
    is_etf = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    last_updated = Column(Date)