import streamlit as st
import pandas as pd
import os
import requests
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

# MySQL 연결
engine = create_engine(DATABASE_URL)

st.set_page_config(page_title="📡 주식 수집 API 연동", layout="wide")
st.title("📡 주식 수집 + 시각화 (FastAPI 연동)")

# 수집 섹션
with st.form(key="collect_form"):
    symbol = st.text_input("종목 코드 (예: AAPL)")
    col1, col2 = st.columns(2)
    with col1:
        start = st.date_input("시작일")
    with col2:
        end = st.date_input("종료일")
    submit = st.form_submit_button("📡 FastAPI로 수집 요청")
    
if submit and symbol:
    with st.spinner("FastAPI로 수집 요청 중..."):
        url = f"http://localhost:8000/collect/{symbol}"
        params = {"start": str(start), "end": str(end)}
        
        try:
            res = requests.post(url, params=params, timeout=20)
            if res.status_code == 200:
                st.success(f"{symbol} 수집 완료: {res.json().get('rows')}건")
            else:
                st.error(f"수집 실패: {res.status_code} / {res.text}")
        
        except requests.exceptions.RequestException as e:
            st.error(f"요청 중 오류 발생: {e}")
            
# 조회 섹션
with st.sidebar:
    st.header("🗂 저장된 종목 보기")
    symbols = pd.read_sql("SELECT DISTINCT symbol FROM stock_prices", engine)
    selected_symbol = st.selectbox("조회할 종목", symbols["symbol"] if not symbols.empty else [])
    
if selected_symbol:
    df = pd.read_sql(
        "SELECT symbol, date, open, high, low, close, volume FROM stock_prices WHERE symbol = %s ORDER BY date DESC",
        engine,
        params=(selected_symbol,)
    )
    st.subheader(f"{selected_symbol} 시세 데이터")
    st.dataframe(df, use_container_width=True)
    st.line_chart(df.sort_values("date")[["date", "close"]].set_index("date"))
    
with st.sidebar:
    st.markdown("### 🔄 NASDAQ 티커 갱신")
    
    if st.button("🆕 종목 티커 갱신"):
        with st.spinner("FastAPI를 통해 NASDAQ 티커 갱신 중..."):
            try:
                res = requests.post("http://localhost:8000/update-tickers", timeout=20)
                if res.status_code == 200:
                    st.success("티커 목록 갱신 완료!")
                else:
                    st.error(f"갱신 실패: {res.status_code} / {res.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"요청 중 오류 발생: {e}")

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
    