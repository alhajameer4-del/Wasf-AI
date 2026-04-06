import streamlit as st
import openai
import requests
import time

# --- 1. المحرك الذكي (The AI Engine) ---
class WasfAI_Engine:
    def __init__(self, api_key):
        openai.api_key = api_key

    def generate_smart_description(self, product_name, category, features, tone):
        prompts = {
            "إلكترونيات": "Focus on technical specs, durability, and innovation.",
            "أزياء وملابس": "Focus on style, comfort, trends, and emotional appeal.",
            "مستحضرات تجميل": "Focus on ingredients, skin benefits, and luxury feel.",
            "عقارات": "Focus on location, investment value, and lifestyle.",
            "خدمات رقمية": "Focus on efficiency, ease of use, and ROI."
        }
        sector_context = prompts.get(category, "Focus on utility and value.")
        
        full_prompt = f"""
        Act as an expert e-commerce copywriter. 
        Product: {product_name}
        Category: {category}
        Features: {features}
        Tone: {tone}
        Guideline: {sector_context}
        Requirement: Write a persuasive product description in Arabic using AIDA model.
        """
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", # أو gpt-4 إذا كان متاحاً لديك
            messages=[{"role": "system", "content": "أنت خبير تسويق رقمي متخصص في المتاجر الإلكترونية."},
                      {"role": "user", "content": full_prompt}]
        )
        return response.choices[0].message.content

# --- 2. نظام التحقق من الدفع (Payment Gateway) ---
def verify_usdt_payment(wallet_address, expected_amount):
    url = f"https://api.trongrid.io/v1/accounts/{wallet_address}/transactions/trc20"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json().get('data', [])
            for tx in data:
                if tx.get('token_info', {}).get('symbol') == 'USDT':
                    amount = float(tx['value']) / 10**6
                    if amount >= expected_amount:
                        return True
    except:
        return False
    return False

# --- 3. واجهة المستخدم (The Dashboard UI) ---
st.set_page_config(page_title="وصْف AI", page_icon="🚀", layout="wide")

# الهوية البصرية
st.title("🚀 وصْف AI: شريكك الذكي في التجارة الإلكترونية")
st.markdown("---")

# القائمة الجانبية
st.sidebar.header("⚙️ إعدادات المتجر")
category = st.sidebar.selectbox("مجال التجارة:", ["إلكترونيات", "أزياء وملابس", "مستحضرات تجميل", "عقارات", "خدمات رقمية"])
tone = st.sidebar.select_slider("نبرة المحتوى:", options=["رسمي", "احترافي", "إبداعي", "حماسي"])

st.sidebar.divider()
st.sidebar.subheader("💳 المحفظة الرقمية")
st.sidebar.write("رصيدك: **0 نقطة**")
if st.sidebar.button("تفعيل الاشتراك (10 USDT)"):
    st.sidebar.code("TGLVcNSTevGibK5Ku3NhHzxQEBxLm7MiSj")
    st.sidebar.info("جاري مراقبة الشبكة للدفع...")

# منطقة العمل الرئيسية
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 مدخلات المنتج")
    product_name = st.text_input("اسم المنتج المعروض:")
    features = st.text_area("المميزات (مثلاً: سريع، مريح، ضمان سنة...):", height=150)
    api_key = st.text_input("أدخل مفتاح OpenAI الخاص بك للبدء:", type="password")

with col2:
    st.subheader("✨ الوصف التسويقي الجاهز")
    if st.button("توليد الوصف بنقرة واحدة"):
        if not api_key:
            st.error("يرجى إدخال مفتاح الـ API أولاً.")
        elif product_name and features:
            with st.spinner('ذكاء وصْف AI يعمل الآن...'):
                try:
                    engine = WasfAI_Engine(api_key)
                    result = engine.generate_smart_description(product_name, category, features, tone)
                    st.success("تم التوليد!")
                    st.write(result)
                    st.download_button("تحميل النص", result)
                except Exception as e:
                    st.error(f"حدث خطأ: {str(e)}")
        else:
            st.warning("أكمل بيانات المنتج أولاً.")

st.markdown("---")
st.caption("حقوق الملكية © 2026 - مشروع وصْف AI للحلول الذكية")
