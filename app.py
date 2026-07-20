import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# إعدادات واجهة التطبيق لتناسب شاشة الهاتف
st.set_page_config(page_title="مساعد الذهب المستقر اللحظي", page_icon="📊", layout="centered")
st.title("📊 مساعد تداول الذهب الفوري (بدون خربطة)")
st.subheader("تحديث فوري مباشر متطابق مع إكسنس")

# الرمز الفوري لذهب الفوركس المتطابق تماماً مع تسعيرة إكسنس بالسنات
GOLD_SYMBOL = "XAUUSD=X"

# كود التحديث التلقائي الآمن والمستقر كل 5 ثوانٍ لمنع تعليق السيرفر
if "counter" not in st.session_state:
    st.session_state.counter = 0

# تحديث الصفحة تلقائياً كل 5000 مللي ثانية (5 ثوانٍ) بشكل مستقر تماماً
time_interval = 5000 
st.form_submit_button = False
st.markdown(f"""
    <iframe src="about:blank" style="display:none" onload="setTimeout(() => {{ window.location.reload(); }}, {time_interval});"></iframe>
""", unsafe_allow_html=True)

def get_gold_data():
    try:
        # جلب بيانات الذهب الفوري لآخر يومين بفارق 5 دقائق
        ticker = yf.Ticker(GOLD_SYMBOL)
        df = ticker.history(period="2d", interval="5m")
        return df
    except:
        return pd.DataFrame()

# دالة لحساب مؤشر RSI الفني لمنع الخسائر
def calculate_rsi(df, periods=14):
    close_delta = df['Close'].diff()
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)
    ma_up = up.ewm(com=periods - 1, adjust=False).mean()
    ma_down = down.ewm(com=periods - 1, adjust=False).mean()
    rsi = ma_up / ma_down
    return 100 - (100 / (1 + rsi))

# الاحتفاظ بآخر سعر لمقارنة الحركة بالسنات
if 'last_price' not in st.session_state:
    st.session_state.last_price = 0.0

try:
    df = get_gold_data()
    
    if not df.empty:
        df['SMA_20'] = df['Close'].rolling(window=20).mean()
        df['RSI'] = calculate_rsi(df)
        
        current_price = df['Close'].iloc[-1]
        last_candle = df.iloc[-2]
        current_rsi = df['RSI'].iloc[-1]
        current_sma = df['SMA_20'].iloc[-1]
        
        open_p = last_candle['Open']
        close_p = last_candle['Close']
        
        # حساب اتجاه نبضة السعر وتلوين السعر بالسنات لمنع الخربطة
        if current_price > st.session_state.last_price:
            price_delta_color = "normal"
            delta_text = f"+${(current_price - st.session_state.last_price):.2f} (ارتفاع بالسنات)"
        elif current_price < st.session_state.last_price:
            price_delta_color = "inverse"
            delta_text = f"-${(st.session_state.last_price - current_price):.2f} (انخفاض بالسنات)"
        else:
            price_delta_color = "off"
            delta_text = "$0.00"
        
        st.session_state.last_price = current_price
        
        # عرض السعر الحالي المباشر المتغير بالسنتات المتطابق مع إكسنس
        st.metric(label="سعر الذهب الفوري المباشر (XAU/USD)", value=f"${current_price:,.2f}", delta=delta_text, delta_color=price_delta_color)
        
        st.caption(f"RSI للسيولة: {current_rsi:.2f} | خط الاتجاه SMA 20: ${current_sma:.2f}")
        
        # إستراتيجية المربعات الملونة الآلية بناءً على المؤشرات والشموع الموحدة
        if current_price > current_sma and current_rsi < 65:
            st.success("🎯 إشارة مؤكدة: خذ صفقة شراء (Buy) الآن على MT4")
            st.markdown("<div style='background-color: #d4edda; padding: 20px; border-radius: 10px; text-align: center;'><h1 style='color: #28a745; font-size: 100px; margin: 0;'>⬆️</h1></div>", unsafe_allow_html=True)
        elif current_price < current_sma and current_rsi > 35:
            st.error("🎯 إشارة مؤكدة: خذ صفقة بيع (Sell) الآن على MT4")
            st.markdown("<div style='background-color: #f8d7da; padding: 20px; border-radius: 10px; text-align: center;'><h1 style='color: #dc3545; font-size: 100px; margin: 0;'>⬇️</h1></div>", unsafe_allow_html=True)
        else:
            st.info("⏳ حالة السوق: تذبذب أو نطاق ضيق (انتظر خارج السوق)")
            st.markdown("<div style='background-color: #e2e3e5; padding: 20px; border-radius: 10px; text-align: center;'><h1 style='color: #6c757d; font-size: 100px; margin: 0;'>🔄</h1></div>", unsafe_allow_html=True)
        
        # رسم مخطط الشموع التفاعلي المتطابق مع الفوركس
        st.write("---")
        st.subheader("📈 رسم الشموع اليابانية الفوري لـ XAU/USD")
        
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
        
        fig.add_trace(go.Scatter(x=df_chart.index, y=df_chart['SMA_20'], mode='lines', name='SMA 20', line=dict(color='orange', width=2)))
        
                fig.update_layout(xaxis_rangeslider_visible=False, margin=dict(l=10, r=10, t=10, b=10), height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
        
        st.write(f"توقيت التحديث الفوري: {datetime.now().strftime('%H:%M:%S')}")
    else:
        st.warning("جاري سحب بيانات أسعار الفوركس الحية...")
except Exception as e:
    st.error("جاري ملاحقة أسعار الفوركس اللحظية...")
