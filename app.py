import streamlit as st
import openai

# --- المحرك الذكي ---
class WasfAI_Engine:
    def __init__(self, api_key):
        openai.api_key = api_key

    def generate_smart_description(self, product_name, features):
        full_prompt = f"اكتب وصف تسويقي جذاب لمنتج: {product_name}. المميزات: {features}. استخدم أسلوب AIDA."
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": full_prompt}]
        )
        return response.choices[0].message.content

# --- واجهة المستخدم ---
st.title("🚀 وصْف AI")

# محاولة سحب المفتاح من الإعدادات السرية (Secrets)
try:
    api_key = st.secrets["OPENAI_API_KEY"]
    engine = WasfAI_Engine(api_key)
    
    product_name = st.text_input("اسم المنتج المعروض:")
    features = st.text_area("المميزات:")

    if st.button("توليد الوصف بنقرة واحدة"):
        if product_name and features:
            with st.spinner('جاري التحليل...'):
                result = engine.generate_smart_description(product_name, features)
                st.success("تم التوليد!")
                st.write(result)
        else:
            st.warning("يرجى ملء البيانات")
except:
    st.error("لم يتم العثور على مفتاح التشغيل في إعدادات Secrets.")
    
