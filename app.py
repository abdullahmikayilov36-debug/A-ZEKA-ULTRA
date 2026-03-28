import streamlit as st
import google.generativeai as genai
import requests
from io import BytesIO
from PIL import Image

# 1. SƏHİFƏ AYARLARI
st.set_page_config(page_title="A-ZEKA INFINITY", page_icon="💠", layout="wide")

# 2. API QOŞULMASI
API_KEY = "AIzaSyByvxHEQfOmuejATOX7JVAXp2gTB27bWdU"
genai.configure(api_key=API_KEY)

# Modelin stabil yüklənməsi
@st.cache_resource
def load_ai():
    return genai.GenerativeModel("gemini-1.5-flash")

model = load_ai()

# 3. ŞƏKİL ÇƏKMƏ MOTORU
def generate_image(prompt):
    try:
        url = f"https://pollinations.ai/p/{prompt.replace(' ', '_')}?width=1024&height=1024&seed=123"
        r = requests.get(url, timeout=15)
        return Image.open(BytesIO(r.content))
    except:
        return None

# 4. YADDAŞ
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- DİZAYN (GÖZƏL VƏ MODERN) ---
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #00ff41; font-family: 'Courier New'; }
    .stChatInput { border-radius: 20px !important; border: 1px solid #00ff41 !important; }
    .stChatMessage { border: 1px solid #00ff41; border-radius: 15px; background: rgba(0,255,65,0.05) !important; }
</style>
""", unsafe_allow_html=True)

st.title("💠 A-ZEKA INFINITY OS")
st.caption("Developed by Abdullah Mikayılov | High-Performance AI")

# Mesajları göstər
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if "img" in m:
            st.image(m["img"])

# 5. ƏSAS İCRA
if prompt := st.chat_input("Sistem əmri gözlənilir..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # ŞƏKİL ÇƏKMƏ KOMANDASI
        if any(word in prompt.lower() for word in ["şəkil", "çək", "draw", "rəsm"]):
            with st.spinner("🎨 Sintez olunur..."):
                img = generate_image(prompt)
                if img:
                    st.image(img)
                    st.session_state.messages.append({"role": "assistant", "content": f"'{prompt}' vizualizasiyası:", "img": img})
                else:
                    st.error("Şəkil mühərriki cavab vermir.")
        else:
            # NORMAL YAZIŞMA
            res_area = st.empty()
            full_res = ""
            try:
                response = model.generate_content(prompt, stream=True)
                for chunk in response:
                    full_res += chunk.text
                    res_area.markdown(full_res + "█")
                st.session_state.messages.append({"role": "assistant", "content": full_res})
            except Exception as e:
                st.error(f"Sistem xətası: {e}")
