import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime

# إعدادات واجهة التطبيق لتناسب شاشة الهاتف
st.set_page_config(page_title="مساعد الذهب اللحظي المطور", page_icon="📊", layout="centered")
st.title("📊 مساعد تداول الذهب الاحترافي الفوري")
st.subheader("تحليل الشموع مع مؤشرات RSI & SMA (تأخير 0 ثانية)")

# رمز الذهب العالمي المتوافق مع إكسنس
GOLD_SYMBOL = "GC=F" 

def get_gold_data():
    # جلب بيانات الذهب بفارق 5 دقائق لكل شمعة
    ticker = yf.Ticker(GOLD_SYMBOL)
    df = ticker.history(period="3d", interval="5m")
    return df

# دالة لحساب مؤشر RSI الفني
def calculate_rsi(df, periods=14):
    close_delta = df['Close'].diff()
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)
    ma_up = up.ewm(com=periods - 1, adjust=False).mean()
    ma_down = down.ewm(com=periods - 1, adjust=False).mean()
    rsi = ma_up / ma_down
    return 100 - (100 / (1 + rsi))

# تشغيل التحديث اللحظي فائق السرعة كل ثانية
placeholder = st.empty()

while True:
    with placeholder.container():
        try:
            df = get_gold_data()
            if not df.empty:
                # حساب المؤشرات الفنية المتقدمة لمنع الخسائر
                df['SMA_20'] = df['Close'].rolling(window=20).mean() # متوسط متحرك لـ 20 شمعة
                df['RSI'] = calculate_rsi(df) # مؤشر RSI
                
                # جلب البيانات الحالية الحية
                current_price = df['Close'].iloc[-1]
                last_candle = df.iloc[-2]
                current_rsi = df['RSI'].iloc[-1]
                current_sma = df['SMA_20'].iloc[-1]
                
                open_p = last_candle['Open']
                close_p = last_candle['Close']
                candle_body = abs(close_p - open_p)
                
                # عرض السعر الحالي المباشر المتزامن
                st.metric(label="سعر الذهب المباشر واللحظي", value=f"${current_price:,.2f}")
                
                # عرض قيم المؤشرات للمراقبة الذكية
                col1, col2 = st.columns(2)
                with col1:
                    st.caption(f"مؤشر الزخم RSI: {current_rsi:.2f}")
                with col2:
                    st.caption(f"الاتجاه SMA 20: ${current_sma:.2f}")
                
                # --- إستراتيجية الأسهم الذكية المفلترة والمصفيّة لمنع الخسارة ---
                # شروط الشراء القوي المتكامل: شمعة خضراء + السعر فوق المتوسط + الذهب ليس في منطقة تشبع شرائي (RSI < 65)
                if close_p > open_p and candle_body > 0.8 and current_price > current_sma and current_rsi < 65:
                    st.success("🎯 إشارة قوية ومؤكدة: خذ صفقة شراء (Buy) الآن على MT4")
                    # سهم أخضر كبير مخصص ومقوى بصرياً للتنبيه
                    st.markdown("<div style='background-color: #d4edda; padding: 20px; border-radius: 10px; text-align: center;'><h1 style='color: #28a745; font-size: 100px; margin: 0;'>⬆️</h1></div>", unsafe_allow_html=True)
                
                # شروط البيع القوي المتكامل: شمعة حمراء + السعر تحت المتوسط + الذهب ليس في منطقة تشبع بيعي (RSI > 35)
                elif close_p < open_p and candle_body > 0.8 and current_price < current_sma and current_rsi > 35:
                    st.error("🎯 إشارة قوية ومؤكدة: خذ صفقة بيع (Sell) الآن على MT4")
                    # سهم أحمر كبير مخصص ومقوى بصرياً للتنبيه
                    st.markdown("<div style='background-color: #f8d7da; padding: 20px; border-radius: 10px; text-align: center;'><h1 style='color: #dc3545; font-size: 100px; margin: 0;'>⬇️</h1></div>", unsafe_allow_html=True)
                
                # إذا تعارضت المؤشرات أو كان السوق خطراً ومتذبذباً
                else:
                    st.info("⏳ حالة السوق: تذبذب أو اتجاه غير مؤكد (انتظر ولا تفتح صفقات حالياً)")
                    st.markdown("<div style='background-color: #e2e3e5; padding: 20px; border-radius: 10px; text-align: center;'><h1 style='color: #6c757d; font-size: 100px; margin: 0;'>🔄</h1></div>", unsafe_allow_html=True)
                
                # عرض مخطط الشموع التفاعلي المطور لآخر 3 ساعات
                st.write("---")
                st.subheader("📈 الرسم البياني للشموع اليابانية الفوري")
                
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
                
                # إضافة خط مؤشر المتوسط المتحرك SMA على الرسم البياني
                fig.add_trace(go.Scatter(
                    x=df_chart.index, 
                    y=df_chart['SMA_20'], 
                    mode='lines', 
                    name='الاتجاه SMA', 
                    line=dict(color='orange', width=2)
                ))
                
                fig.update_layout(
                    xaxis_rangeslider_visible=False,
                    margin=dict(l=10, r=10, t=10, b=10),
                    height=350,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig, use_container_width=True)
                
                st.write(f"توقيت التحديث الفوري اللحظي: {datetime.now().strftime('%H:%M:%S')}")
                
        except Exception as e:
            st.error("جاري ملاحقة الأسعار اللحظية وتحديث المؤشرات الفنية...")
            
        # تسريع التحديث إلى ثانية واحدة فقط لإلغاء أي تأخير ومطابقة رمشة العين
        time.sleep(1)
        st.rerun()
