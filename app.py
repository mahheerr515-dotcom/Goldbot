import streamlit as st
import yfinance as yf
import pandas as pd
import time

# إعدادات واجهة التطبيق
st.set_page_config(page_title="مساعد تداول الذهب", page_icon="📊", layout="centered")
st.title("📊 مساعد تداول الذهب المخصص (إكسنس)")
st.subheader("تحليل الشموع الحية وإشارات الأسهم")

# تحديد رمز الذهب (متوافق مع الأسعار العالمية)
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
                high_p = last_candle['High']
                low_p = last_candle['Low']
                
                # حساب حجم الشمعة وتحليلها
                candle_body = abs(close_p - open_p)
                
                st.metric(label="سعر الذهب الحالي الحقيقي", value=f"${current_price:,.2f}")
                st.write(f"تحليل آخر شمعة 5 دقائق مكتملة:")
                
                # إستراتيجية تحليل الشموع (برايس أكشن مبسط)
                if close_p > open_p and candle_body > 1.5:
                    # شمعة خضراء صاعدة وقوية
                    st.success("📈 إشارة: صعود متوقع! (خذ صفقة شراء على MT4)")
                    st.markdown("<h1 style='text-align: center; color: green; font-size: 100px;'>⬆️</h1>", unsafe_allow_html=True)
                
                elif close_p < open_p and candle_body > 1.5:
                    # شمعة حمراء هابطة وقوية
                    st.error("📉 إشارة: هبوط متوقع! (خذ صفقة بيع على MT4)")
                    st.markdown("<h1 style='text-align: center; color: red; font-size: 100px;'>⬇️</h1>", unsafe_allow_html=True)
                
                else:
                    # السوق متذبذب أو الشموع صغيرة
                    st.info("⏳ حالة السوق: تذبذب (انتظر ولا تأخذ صفقة حالياً)")
                    st.markdown("<h1 style='text-align: center; color: gray; font-size: 100px;'>🔄</h1>", unsafe_allow_html=True)
                    
                # عرض جدول البيانات البسيط للمراقبة
                st.write("تفاصيل آخر شمعة:")
                st.write(f"الافتتاح: ${open_p:.2f} | الإغلاق: ${close_p:.2f}")
                
        except Exception as e:
            st.error("جاري الاتصال بمزود الأسعار الحية...")
            
        # تحديث البرنامج كل 10 ثوانٍ لملاحقة السعر
        time.sleep(10)
        st.rerun()
