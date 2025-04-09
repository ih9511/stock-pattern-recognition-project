from datetime import datetime
import pandas as pd
import yfinance as yf

from app.database import SessionLocal
from app.models import StockPrice

def flatten_columns(df: pd.DataFrame) -> pd.DataFrame:
    new_columns = []
    for col in df.columns:
        if isinstance(col, tuple):
            new_columns.append(col[0]) # ('Open', 'APPL') -> 'Open'
        else:
            new_columns.append(col)

    df.columns = new_columns

    return df

def fetch_stock_data(symbol: str, start: str, end: str) -> pd.DataFrame:
    df = yf.download(symbol, start=start, end=end)
    df.reset_index(inplace=True)

    # Flatten columns if MultiIndex
    df = flatten_columns(df)

    df['symbol'] = symbol

    return df[['symbol', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume']]

def insert_data(df: pd.DataFrame):
    session = SessionLocal()
    try:
        for _, row in df.iterrows():
            symbol_value = str(row['symbol']) if not isinstance(row['symbol'], str) else row['symbol']

            item = StockPrice(
                symbol=symbol_value,
                date=row['Date'].date(),
                open=row['Open'],
                high=row['High'],
                low=row['Low'],
                close=row['Close'],
                volume=int(row['Volume']),
            )
            session.merge(item) # 이미 있는 데이터는 업데이트
        session.commit()
        print(f"{len(df)} rows inserted.")
    
    except Exception as e:
        session.rollback()
        print("Error:", e)
    
    finally:
        session.close()


if __name__ == "__main__":
    df = fetch_stock_data("AAPL", "2023-01-01", "2023-03-31")
    insert_data(df)