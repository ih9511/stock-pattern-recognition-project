import pandas as pd
import os
from datetime import date
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from .models import StockTicker
from .database import SessionLocal

load_dotenv()

NASDAQ_URL = os.getenv("NASDAQ_URL")
NYSE_URL = os.getenv("NYSE_URL")
GITHUB_NASDAQ_TICKER_URL = os.getenv("GITHUB_NASDAQ_TICKER_URL")

def fetch_nasdaq_tickers_from_github() -> pd.DataFrame:
    df = pd.read_csv(GITHUB_NASDAQ_TICKER_URL)
    df = df.rename(columns={
        "Symbol": "symbol",
        "Company Name": "name",
        "ETF": "is_etf",
    })

    df["exchange"] = "NASDAQ"
    df["is_etf"] = df["is_etf"].astype(str).str.upper() == "Y"
    df["is_active"] = True
    df["last_updated"] = date.today()
    
    # 결측값 제거
    df = df.dropna(subset=['symbol', 'name'])
    df = df[df['symbol'].str.strip() != '']

    return df[["symbol", "name", "exchange", "is_etf", "is_active", "last_updated"]]

def update_stock_tickers():
    df = fetch_nasdaq_tickers_from_github()
    session: Session = SessionLocal()
    try:
        for _, row in df.iterrows():
            ticker = StockTicker(
                symbol=row["symbol"],
                name=row["name"],
                exchange=row["exchange"],
                is_etf=row["is_etf"],
                is_active=row["is_active"],
                last_updated=row["last_updated"]
            )
            session.merge(ticker)
        session.commit()
        print(f"{len(df)} NASDAQ tickers inserted or updated.")
    except Exception as e:
        session.rollback()
        print("Ticker update failed:", e)
    finally:
        session.close()