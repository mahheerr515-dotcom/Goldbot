import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime

# إعدادات واجهة التطبيق
st.set_page_config(page_title="مساعد تداول الذهب السريع", page_icon="📊", layout="centered")
st.title("📊 مساعد تداول الذهب المخصص (إكسنس)")
st.subheader("تحليل الشموع الحية والرسوم البيانية")

# تحديد رمز الذهب العالمي المتوافق تماماً مع إكسنس
GOLD_SYMBOL = "GC=F" 

def get_gold_data():
    # جلب بيانات الذهب لآخر يومين بفارق 5 دقائق لكل شمعة
    ticker = yf.Ticker(GOLD_SYMBOL)
    df = ticker.history(period="2d", interval="5m")
    return df

# تحديث تلقائي فائق السرعة للبيانات
placeholder = st.empty()

while True:
    with placeholder.container():
        try:
            df = get_gold_data()
            if not df.empty:
                current_price = df['Close'].iloc[-1]
                last_candle = df.iloc[-2]
                
                open_p = last_candle['Open']
                close_p = last_candle['Close']
                candle_body = abs(close_p - open_p)
                
                # عرض السعر الحالي المباشر
                st.metric(label="سعر الذهب الحالي الحقيقي", value=f"${current_price:,.2f}")
                
                # إستراتيجية تحليل الشموع لتوليد إشارات الأسهم
                if close_p > open_p and candle_body > 1.0:
                    st.success("📈 إشارة: صعود متوقع! (خذ صفقة شراء على MT4)")
                    st.markdown("<h1 style='text-align: center; color: green; font-size: 80px;'>⬆️</h1>", unsafe_allow_html=True)
                elif close_p < open_p and candle_body > 1.0:
                    st.error("📉 إشارة: هبوط متوقع! (خذ صفقة بيع على MT4)")
                    st.markdown("<h1 style='text-align: center; color: red; font-size: 80px;'>⬇️</h1>", unsafe_allow_html=True)
                else:
                    st.info("⏳ حالة السوق: تذبذب (انتظر ولا تأخذ صفقة حالياً)")
                    st.markdown("<h1 style='text-align: center; color: gray; font-size: 80px;'>🔄</h1>", unsafe_allow_html=True)
                
                # عرض الشموع اليابانية التفاعلية لآخر 3 ساعات
                st.write("---")
                st.subheader("📈 الرسم البياني للشموع اليابانية (آخر 3 ساعات)")
                
                df_chart = df.tail(36)
                fig = go.Figure(data=[go.Candlestick(
                    x=df_chart.index,
                    open=df_chart['Open'],
                    high=df_chart['High'],
                    low=df_chart['Low'],
                    close=df_chart['Close'],
                    increasing_line_color='green',
                    decreasing_line_color='red'
                )])
                
                fig.update_layout(
                    xaxis_rangeslider_visible=False,
                    margin=dict(l=10, r=10, t=10, b=10),
                    height=350,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig, use_container_width=True)
                
                st.write(f"توقيت آخر تحديث: {datetime.now().strftime('%H:%M:%S')}")
                
        except Exception as e:
            st.error("جاري التحديث التلقائي للأسعار الحية...")
            
        # جعل التحديث سريعاً جداً كل 5 ثوانٍ فقط لملاحقة حركة السعر بدقة
        time.sleep(5)
        st.rerun()
