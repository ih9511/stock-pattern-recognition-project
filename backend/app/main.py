"""FastAPI 엔트리 포인트"""
from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.collector import fetch_stock_data
from app.crud import insert_data

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/collect/{symbol}")
def collect(symbol: str, start: str = Query(...), end: str = Query(...), db: Session = Depends(get_db)):
    df = fetch_stock_data(symbol, start, end)
    row_count = insert_data(df, db)
    
    return {"message": f"{symbol} 수집 완료", "rows": row_count}