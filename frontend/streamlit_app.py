import streamlit as st
import pandas as pd
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

# MySQL 연결
engine = create_engine(DATABASE_URL)

# 종목 목록 가져오기
@st.cache_data
def get_symbols():
    with engine.connect() as conn:
        query = "SELECT DISTINCT symbol FROM stock_prices"
        result = conn.execute(text(query))
        return [row[0] for row in result.fetchall()]
    
# 특정 종목 데이터 가져오기
@st.cache_data
def get_stock_data(symbol):
    query = f"""
        SELECT date, open, high, low, close, volume
        FROM stock_prices
        WHERE symbol = %s
        ORDER BY date DESC
    """
    df = pd.read_sql(query, engine, params=(symbol,))

    return df

# UI
st.title("📈 주식 DB 뷰어")

symbols = get_symbols()
if not symbols:
    st.warning("DB에 저장된 종목이 없습니다.")
else:
    selected_symbol = st.selectbox("종목 선택", symbols)
    df = get_stock_data(selected_symbol)

    st.subheader(f"{selected_symbol} 데이터 미리보기")
    st.dataframe(df, use_container_width=True)