import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. SƏHİFƏ AYARLARI
st.set_page_config(page_title="A-ZEKA Pro", page_icon="⚡", layout="wide")

# 2. API TƏNZİMLƏMƏLƏRİ
# Bu səfər heç bir əlavə parametr qoymadan ən sadə yolla qoşuluruq
API_KEY = "AIzaSyCIwmGxUyFH9IbLd1yF_LuUPK11rCtkuss"
genai.configure(api_key=API_KEY)

# 3. MODELİN TƏYİNİ (Xətasız Versiya)
# Burada models/ ön şəkilçisini sildik ki, 404 verməsin
try:
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error(f"Model qoşulma xətası: {e}")

# 4. YADDAŞ
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- 5. DİZAYN VƏ İNTERFEYS ---
with st.sidebar:
    st.title("⚙️ A-ZEKA Ayarları")
    if st.button("🗑️ Tarixçəni Sil", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()
    st.divider()
    uploaded_file = st.file_uploader("Şəkil analizi (Könüllü)", type=["png", "jpg", "jpeg"])

st.title("⚡ A-ZEKA Ultra")
st.caption("Dünyanın ən mürəkkəb sualları üçün hazırlanmış stabil versiya.")

# Mesajları göstər
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Sual daxil etmə
if user_input := st.chat_input("Sualınızı yazın..."):
    st.chat_message("user").markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    with st.chat_message("assistant"):
        with st.spinner("A-ZEKA cavab verir..."):
            try:
                # Şəkil varsa başqa, yoxdursa başqa model (Vision dəstəyi üçün)
                if uploaded_file:
                    vision_model = genai.GenerativeModel('gemini-pro-vision')
                    img = Image.open(uploaded_file)
                    response = vision_model.generate_content([user_input, img])
                else:
                    response = model.generate_content(user_input)
                
                st.markdown(response.text)
                st.session_state.chat_history.append({"role": "assistant", "content": response.text})
                
            except Exception as e:
                st.error(f"Bağlantı xətası: {e}")
                st.info("Məsləhət: API açarının aktivləşməsi üçün 5 dəqiqə gözləyib səhifəni yeniləyin.")
