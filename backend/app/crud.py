"""DB 삽입 로직 분리"""
from sqlalchemy.orm import Session
from datetime import datetime
from app.models import StockPrice
import pandas as pd

def insert_data(df: pd.DataFrame, session: Session):
    for _, row in df.iterrows():
        symbol_value = str(row['symbol']) if not isinstance(row['symbol'], str) else row['symbol']
        date_value = row['Date']
        if isinstance(date_value, pd.Timestamp):
            date_value = date_value.date()

        volume_value = row['Volume']
        if pd.isna(volume_value):
            volume_value = 0

        else:
            volume_value = int(volume_value)

        item = StockPrice(
            symbol=symbol_value,
            date=date_value,
            open=row['Open'],
            high=row['High'],
            low=row['Low'],
            close=row['Close'],
            volume=volume_value,
        )
        session.merge(item)
    session.commit()
    return len(df)