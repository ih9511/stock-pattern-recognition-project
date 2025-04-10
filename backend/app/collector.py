"""수집 관련 로직 분리"""
import pandas as pd
import yfinance as yf

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