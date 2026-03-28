import streamlit as st
import google.generativeai as genai
import requests
import io
import time
from PIL import Image, ImageEnhance, ImageFilter
from datetime import datetime

# ==============================================================================
# 1. ULTRA MODERN WHITE MODE DIZAYN
# ==============================================================================
st.set_page_config(page_title="A-ZEKA PRO MAX", page_icon="🤖", layout="wide")

st.markdown("""
<style>
    /* Təmiz Ağ Dizayn */
    .stApp { background-color: #FFFFFF; color: #1A1A1A; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    
    /* Yan Menyu */
    [data-testid="stSidebar"] { background-color: #F8F9FA; border-right: 1px solid #E0E0E0; }
    
    /* Mesaj qutularının forması */
    .stChatMessage { border-radius: 15px !important; padding: 15px !important; margin-bottom: 10px !important; border: 1px solid #F0F2F6 !important; }
    
    /* Süni İntellektin cavab sahəsi */
    [data-testid="stChatMessageAssistant"] { background-color: #FFFFFF !important; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
    
    /* Giriş paneli */
    .stChatInput { border-radius: 12px !important; border: 1px solid #DEDEDE !important; }
    
    /* Mətn rəngləri */
    h1, h2, h3, p { color: #1A1A1A !important; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. İNTELLEKTUAL KONFİQURASİYA
# ==============================================================================
API_KEY = "AIzaSyByvxHEQfOmuejATOX7JVAXp2gTB27bWdU"
genai.configure(api_key=API_KEY)

# A-ZEKA Təlimatnaməsi
instruction = (
    "Sən A-ZEKA-san. Dünyanın ən vəhşi və sürətli intellektisən. "
    "Yaradıcın Abdullah Mikayılovdur. Bütün riyazi düsturları LaTeX ($...$) ilə göstər. "
    "Azərbaycan dilində qüsursuz və professional cavablar ver."
)

@st.cache_resource
def load_ai_engine():
    return genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=instruction
    )

model = load_ai_engine()

# ==============================================================================
# 3. VƏHŞİ FUNKSİYALAR (ŞƏKİL ÇƏKMƏ VƏ ANALİZ)
# ==============================================================================

def draw_art(prompt):
    try:
        url = f"https://pollinations.ai/p/{prompt.replace(' ', '_')}?width=1024&height=1024&nologo=true"
        r = requests.get(url, timeout=20)
        return Image.open(io.BytesIO(r.content))
    except:
        return None

# ==============================================================================
# 4. İNTERFEYS (UI)
# ==============================================================================

# YAN PANEL (SIDEBAR)
with st.sidebar:
    st.title("⚙️ A-ZEKA Ayarlar")
    st.write(f"Xoş gəldin, **Abdullah**!")
    
    st.divider()
    
    # SƏNİN İSTƏDİYİN O '+' DÜYMƏSİ (FILE UPLOADER)
    st.subheader("➕ Şəkil Əlavə Et")
    uploaded_file = st.file_uploader("Analiz üçün şəkil yüklə", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file:
        st.image(uploaded_file, caption="Yüklənilən Fayl", use_container_width=True)
    
    st.divider()
    
    if st.button("🗑️ Söhbəti Təmizlə", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

# ƏSAS SƏHİFƏ
st.title("🤖 A-ZEKA PRO MAX")
st.write("Sistem Statusu: **Vəhşi Rejim Aktiv** ✅")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Mesajları göstər
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "img" in msg:
            st.image(msg["img"])

# ==============================================================================
# 5. İCRA MOTORU
# ==============================================================================

if prompt := st.chat_input("Sualınızı və ya şəkil əmrinizi bura yazın..."):
    # İstifadəçi mesajı
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Süni İntellektin Cavabı
    with st.chat_message("assistant"):
        res_box = st.empty()
        full_ans = ""
        
        try:
            # ŞƏKİL ÇƏKMƏ ŞƏRTİ
            if any(k in prompt.lower() for k in ["çək", "yarat", "şəkil", "draw"]):
                with st.spinner("🎨 A-ZEKA rəsm çəkir..."):
                    img = draw_art(prompt)
                    if img:
                        st.image(img)
                        full_ans = f"İstədiyiniz '{prompt}' şəklini hazırladım."
                        st.session_state.chat_history.append({"role": "assistant", "content": full_ans, "img": img})
                    else:
                        st.error("Şəkil mühərriki qoşulmadı.")
            
            # ŞƏKİL ANALİZİ (ƏGƏR ŞƏKİL YÜKLƏNİBSƏ)
            elif uploaded_file:
                with st.spinner("🔍 Şəkil təhlil edilir..."):
                    img_pil = Image.open(uploaded_file)
                    response = model.generate_content([prompt, img_pil])
                    full_ans = response.text
                    res_box.markdown(full_ans)
                    st.session_state.chat_history.append({"role": "assistant", "content": full_ans})
            
            # NORMAL SÖHBƏT
            else:
                response = model.generate_content(prompt, stream=True)
                for chunk in response:
                    full_ans += chunk.text
                    res_box.markdown(full_ans + " ▌")
                res_box.markdown(full_ans)
                st.session_state.chat_history.append({"role": "assistant", "content": full_ans})
                
        except Exception as e:
            st.error(f"⚠️ Xəta: {e}")
