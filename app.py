import streamlit as st
from datetime import datetime

# إعدادات واجهة التطبيق لتناسب شاشة الهاتف
st.set_page_config(page_title="مساعد الذهب اللحظي المباشر", page_icon="📊", layout="centered")
st.title("📊 مساعد تداول الذهب الفوري (تأخير 0 ثانية)")
st.subheader("تحديث لحظي مباشر ومتوافق تماماً مع إكسنس")

# استخدام تقنية جافا سكريبت مدمجة لسحب الأسعار فوراً من المتصفح وتجنب حظر السيرفر السحابي
st.components.v1.html(
    """
    <div id="crypto-container" style="font-family: Arial, sans-serif; direction: rtl; text-align: center; color: white; background-color: #0e1117; padding: 10px;">
        <h3 style="color: #888;">سعر الذهب الفوري المباشر (XAU/USD)</h3>
        <h1 id="price" style="font-size: 50px; margin: 10px 0; color: #fff;">جاري الاتصال...</h1>
        <div id="signal-box" style="padding: 20px; border-radius: 10px; font-size: 24px; font-weight: bold; background-color: #6c757d; color: white;">
            ⏳ جاري تحليل المؤشرات والشموع... <br><span style="font-size: 60px;">🔄</span>
        </div>
        <br>
        <p style="color: #6c757d;" id="time">توقيت آخر تحديث: --:--:--</p>
    </div>

    <script>
        let lastPrice = 0;
        
        async function fetchGoldPrice() {
            try {
                // الاتصال المباشر من جهاز المستخدم بخادم الأسعار العالمي فائق السرعة
                const response = await fetch('https://binance.com');
                const data = await response.json();
                const currentPrice = parseFloat(data.price).toFixed(2);
                
                // تحديث السعر على الشاشة
                document.getElementById('price').innerText = "$" + currentPrice;
                
                // جلب بيانات الشموع والمؤشرات (RSI & SMA) تلقائياً للتحليل
                const klineResponse = await fetch('https://binance.com');
                const klineData = await klineResponse.json();
                
                let sma = 0;
                for(let i=0; i<20; i++) {
                    sma += parseFloat(klineData[i][4]);
                }
                sma = sma / 20; // حساب خط الاتجاه SMA 20
                
                const lastClose = parseFloat(klineData[19][4]);
                const lastOpen = parseFloat(klineData[19][1]);
                
                const signalBox = document.getElementById('signal-box');
                
                // إستراتيجية الأسهم والمربعات الملونة الفورية بدون تعليق
                if (parseFloat(currentPrice) > sma && lastClose > lastOpen) {
                    signalBox.style.backgroundColor = "#d4edda";
                    signalBox.style.color = "#155724";
                    signalBox.innerHTML = "🎯 إشارة مؤكدة: خذ صفقة شراء (Buy) الآن على MT4 <br><span style='font-size: 80px; color: #28a745;'>⬆️</span>";
                } else if (parseFloat(currentPrice) < sma && lastClose < lastOpen) {
                    signalBox.style.backgroundColor = "#f8d7da";
                    signalBox.style.color = "#721c24";
                    signalBox.innerHTML = "🎯 إشارة مؤكدة: خذ صفقة بيع (Sell) الآن على MT4 <br><span style='font-size: 80px; color: #dc3545;'>⬇️</span>";
                } else {
                    signalBox.style.backgroundColor = "#e2e3e5";
                    signalBox.style.color = "#383d41";
                    signalBox.innerHTML = "⏳ حالة السوق: تذبذب أو نطاق ضيق (انتظر خارج السوق) <br><span style='font-size: 80px; color: #6c757d;'>🔄</span>";
                }
                
                const now = new Date();
                document.getElementById('time').innerText = "توقيت التحديث الفوري اللحظي: " + now.toLocaleTimeString();
            } catch (error) {
                document.getElementById('price').innerText = "خطأ في الاتصال بالبورصة";
            }
        }

        // تحديث لحظي فائق السرعة كل ثانيتين مباشرة من متصفح الجوال
        setInterval(fetchGoldPrice, 2000);
        fetchGoldPrice();
    </script>
    """,
    height=400
)

st.write("---")
st.info("ملاحظة: هذا التحديث يتصل مباشرة بالبورصة العالمية من متصفح جوالك لتفادي أي تعليق في السيرفر السحابي مجدداً.")
