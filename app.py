import streamlit as st
import google.generativeai as genai
import time
import requests
from io import BytesIO
from PIL import Image
from datetime import datetime

# 1. KONFİQURASİYA
st.set_page_config(page_title="A-ZEKA INFINITY", page_icon="💠", layout="wide")

# 2. API QOŞULMASI
API_KEY = "AIzaSyByvxHEQfOmuejATOX7JVAXp2gTB27bWdU"
genai.configure(api_key=API_KEY)

# Modelin yüklənməsi
@st.cache_resource
def load_model():
    return genai.GenerativeModel("gemini-1.5-flash")

model = load_model()

# 3. ŞƏKİL ÇƏKMƏ FUNKSİYASI
def draw_now(prompt):
    try:
        url = f"https://pollinations.ai/p/{prompt.replace(' ', '_')}?width=1024&height=1024"
        r = requests.get(url, timeout=15)
        return Image.open(BytesIO(r.content))
    except:
        return None

# 4. YADDAŞ SİSTEMİ
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- DİZAYN (CSS) ---
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #00ff41; }
    .stChatMessage { border: 1px solid #00ff41; border-radius: 10px; background: rgba(0,255,65,0.05) !important; }
</style>
""", unsafe_allow_html=True)

st.title("💠 A-ZEKA INFINITY OS")

# Mesajları göstər
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if "img" in m:
            st.image(m["img"])

# 5. ƏSAS MOTOR
if prompt := st.chat_input("Komanda daxil edin..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if any(x in prompt.lower() for x in ["şəkil", "çək", "draw"]):
            with st.spinner("🎨 Şəkil sintez olunur..."):
                img = draw_now(prompt)
                if img:
                    st.image(img)
                    st.session_state.messages.append({"role": "assistant", "content": f"'{prompt}' üçün şəkil hazırlandı.", "img": img})
                else:
                    st.error("Şəkil mühərriki qoşulmadı.")
        else:
            res_area = st.empty()
            full_res = ""
            try:
                response = model.generate_content(prompt, stream=True)
                for chunk in response:
                    full_res += chunk.text
                    res_area.markdown(full_res + "█")
                st.session_state.messages.append({"role": "assistant", "content": full_res})
            except Exception as e:
                st.error(f"Xəta: {e}")
