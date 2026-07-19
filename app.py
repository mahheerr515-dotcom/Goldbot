import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time

# إعدادات واجهة التطبيق
st.set_page_config(page_title="مساعد تداول الذهب المطور", page_icon="📊", layout="centered")
st.title("📊 مساعد تداول الذهب المخصص (إكسنس)")
st.subheader("تحليل الشموع الحية والرسوم البيانية")

# تحديد رمز الذهب
GOLD_SYMBOL = "GC=F" 

def get_gold_data():
    # جلب بيانات الذهب لآخر يومين بفارق 5 دقائق لكل شمعة
    ticker = yf.Ticker(GOLD_SYMBOL)
    df = ticker.history(period="2d", interval="5m")
    return df

# تحديث تلقائي للبيانات
placeholder = st.empty()

while True:
    with placeholder.container():
        try:
            df = get_gold_data()
            if not df.empty:
                # جلب بيانات آخر شمعة مكتملة والشمعة الحالية
                last_candle = df.iloc[-2]
                current_price = df['Close'].iloc[-1]
                
                open_p = last_candle['Open']
                close_p = last_candle['Close']
                
                # حساب حجم الشمعة وتحليلها
                candle_body = abs(close_p - open_p)
                
                # عرض السعر الحالي والإشارة الرقمية
                st.metric(label="سعر الذهب الحالي الحقيقي", value=f"${current_price:,.2f}")
                
                # إستراتيجية تحليل الشموع (برايس أكشن) لإظهار الأسهم التنبيهية
                if close_p > open_p and candle_body > 1.5:
                    st.success("📈 إشارة: صعود متوقع! (خذ صفقة شراء على MT4)")
                    st.markdown("<h1 style='text-align: center; color: green; font-size: 80px;'>⬆️</h1>", unsafe_allow_html=True)
                elif close_p < open_p and candle_body > 1.5:
                    st.error("📉 إشارة: هبوط متوقع! (خذ صفقة بيع على MT4)")
                    st.markdown("<h1 style='text-align: center; color: red; font-size: 80px;'>⬇️</h1>", unsafe_allow_html=True)
                else:
                    st.info("⏳ حالة السوق: تذبذب (انتظر ولا تأخذ صفقة حالياً)")
                    st.markdown("<h1 style='text-align: center; color: gray; font-size: 80px;'>🔄</h1>", unsafe_allow_html=True)
                
                # --- إضافة ميزة الشموع اليابانية التفاعلية ---
                st.write("---")
                st.subheader("📈 الرسم البياني للشموع اليابانية (آخر 3 ساعات)")
                
                # أخذ آخر 36 شمعة لعرض تفاصيل واضحة على الجوال
                df_chart = df.tail(36)
                
                fig = go.Figure(data=[go.Candlestick(
                    x=df_chart.index,
                    open=df_chart['Open'],
                    high=df_chart['High'],
                    low=df_chart['Low'],
                    close=df_chart['Close'],
                    increasing_line_color='green',  # الشموع الصاعدة باللون الأخضر
                    decreasing_line_color='red'     # الشموع الهابطة باللون الأحمر
                )])
                
                # تحسين إعدادات الرسم البياني ليناسب شاشة الهاتف
                fig.update_layout(
                    xaxis_rangeslider_visible=False, # إخفاء شريط التمرير السفلي لمنع تشتت الشاشة
                    margin=dict(l=10, r=10, t=10, b=10),
                    height=350,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                
                # عرض الرسم البياني للشموع على الواجهة
                st.plotly_chart(fig, use_container_width=True)
                
                # تفاصيل رقمية سريعة أسفل الشموع
                st.write(f"**آخر افتتاح:** ${open_p:.2f} | **آخر إغلاق:** ${close_p:.2f}")
                
        except Exception as e:
            st.error("جاري الاتصال بمزود الأسعار الحية وتحديث الشموع...")
            
        # تحديث البرنامج كل 10 ثوانٍ لملاحقة حركة السعر والشموع
        time.sleep(10)
        st.rerun()
