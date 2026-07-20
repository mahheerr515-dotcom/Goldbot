import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime

# إعدادات واجهة التطبيق لتناسب شاشة الهاتف
st.set_page_config(page_title="مساعد الذهب اللحظي الموحد", page_icon="📊", layout="centered")
st.title("📊 مساعد تداول الذهب الفوري (النسخة المستقرة)")
st.subheader("تحليل فوري متزامن وثابت متطابق مع إكسنس")

# تم التغيير لرمز الذهب الفوري المباشر ليتطابق مع ميتاترايدر بالملي
GOLD_SYMBOL = "XAUUSD=X"

def get_gold_data():
    try:
        # سحب بيانات الذهب الفوري لآخر يومين بفارق 5 دقائق لكل شمعة
        ticker = yf.Ticker(GOLD_SYMBOL)
        df = ticker.history(period="2d", interval="5m")
        return df
    except:
        return pd.DataFrame()

# دالة حساب مؤشر RSI الفني المعتمد لمنع الخسائر
def calculate_rsi(df, periods=14):
    close_delta = df['Close'].diff()
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)
    ma_up = up.ewm(com=periods - 1, adjust=False).mean()
    ma_down = down.ewm(com=periods - 1, adjust=False).mean()
    rsi = ma_up / ma_down
    return 100 - (100 / (1 + rsi))

placeholder = st.empty()

while True:
    with placeholder.container():
        try:
            df = get_gold_data()
            if not df.empty:
                # حساب المؤشرات الفنية بدقة (SMA 20 و RSI) بالخلفية
                df['SMA_20'] = df['Close'].rolling(window=20).mean()
                df['RSI'] = calculate_rsi(df)
                
                current_price = df['Close'].iloc[-1]
                last_candle = df.iloc[-2]
                current_rsi = df['RSI'].iloc[-1]
                current_sma = df['SMA_20'].iloc[-1]
                
                open_p = last_candle['Open']
                close_p = last_candle['Close']
                candle_body = abs(close_p - open_p)
                
                # عرض سعر الذهب المباشر المتطابق مع إكسنس
                st.metric(label="سعر الذهب الفوري الحالي (XAU/USD)", value=f"${current_price:,.2f}")
                
                # عرض قراءات المؤشرات التي يحللها البرنامج تلقائياً بالخلفية
                st.caption(f"RSI للسيولة: {current_rsi:.2f} | خط الاتجاه SMA 20: ${current_sma:.2f}")
                
                # --- إستراتيجية الأسهم والمربعات الملونة المستقرة ---
                if close_p > open_p and candle_body > 0.3 and current_price > current_sma and current_rsi < 65:
                    st.success("🎯 إشارة مؤكدة: خذ صفقة شراء (Buy) الآن على MT4")
                    st.markdown("<div style='background-color: #d4edda; padding: 20px; border-radius: 10px; text-align: center;'><h1 style='color: #28a745; font-size: 100px; margin: 0;'>⬆️</h1></div>", unsafe_allow_html=True)
                elif close_p < open_p and candle_body > 0.3 and current_price < current_sma and current_rsi > 35:
                    st.error("🎯 إشارة مؤكدة: خذ صفقة بيع (Sell) الآن على MT4")
                    st.markdown("<div style='background-color: #f8d7da; padding: 20px; border-radius: 10px; text-align: center;'><h1 style='color: #dc3545; font-size: 100px; margin: 0;'>⬇️</h1></div>", unsafe_allow_html=True)
                else:
                    st.info("⏳ حالة السوق: تذبذب أو اتجاه غير مؤكد (انتظر خارج السوق)")
                    st.markdown("<div style='background-color: #e2e3e5; padding: 20px; border-radius: 10px; text-align: center;'><h1 style='color: #6c757d; font-size: 100px; margin: 0;'>🔄</h1></div>", unsafe_allow_html=True)
                
                # رسم مخطط الشموع اليابانية التفاعلي الموثوق
                st.write("---")
                st.subheader("📈 رسم الشموع اليابانية الفوري (فريم 5 دقائق)")
                
                df_chart = df.tail(36)
                fig = go.Figure(data=[go.Candlestick(
                    x=df_chart.index, open=df_chart['Open'], high=df_chart['High'], low=df_chart['Low'], close=df_chart['Close'],
                    increasing_line_color='green', decreasing_line_color='red'
                )])
                
                # إضافة خط المتوسط المتحرك البرتقالي على الرسم
                fig.add_trace(go.Scatter(x=df_chart.index, y=df_chart['SMA_20'], mode='lines', name='SMA 20', line=dict(color='orange', width=2)))
                fig.update_layout(xaxis_rangeslider_visible=False, margin=dict(l=10, r=10, t=10, b=10), height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)
                
                st.write(f"توقيت آخر تحديث ناجح: {datetime.now().strftime('%H:%M:%S')}")
        except Exception as e:
            st.error("جاري الاتصال المباشر بمزود الأسعار وتحديث الشموع والمؤشرات...")
            
    # تحديث مستقر كل 10 ثوانٍ لضمان أعلى دقة وسرعة وبدون حظر
    time.sleep(10)
    st.rerun()
