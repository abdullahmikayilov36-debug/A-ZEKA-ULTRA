import streamlit as st
import google.generativeai as genai
import time
import requests
import json
import random
import os
from io import BytesIO
from PIL import Image, ImageEnhance, ImageFilter
from datetime import datetime

# ==============================================================================
# SİSTEMİN NÜVƏSİ - A-ZEKA OS v4.0 (ULTRA EXPANDED EDITION)
# ==============================================================================

# 1. GLOBAL KONFİQURASİYA VƏ VİZUAL MATRİS
st.set_page_config(
    page_title="A-ZEKA INFINITY OS",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. CYBER-CORE UI (MİNİMALİST VƏ GÜCLÜ CSS)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@300;500&display=swap');
    
    body { font-family: 'Fira Code', monospace; }
    .stApp { background: #050505; color: #00ff41; }
    
    /* Terminal Tərzli Mesajlar */
    .stChatMessage {
        border: 1px solid #00ff41;
        background: rgba(0, 50, 0, 0.1) !important;
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.2);
        border-radius: 5px !important;
        animation: glow 2s infinite alternate;
    }
    
    @keyframes glow {
        from { box-shadow: 0 0 5px #00ff41; }
        to { box-shadow: 0 0 20px #00ff41; }
    }

    /* Neon Düymələr */
    .stButton>button {
        width: 100%;
        background: transparent;
        color: #00ff41;
        border: 1px solid #00ff41;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: #00ff41;
        color: black;
        box-shadow: 0 0 30px #00ff41;
    }
    
    /* Yan menyu stili */
    [data-testid="stSidebar"] {
        background-color: #0a0a0a;
        border-right: 1px solid #00ff41;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. İNTELLEKTUAL MOTOR (GEMINI CORE)
# ==============================================================================
API_KEY = "AIzaSyByvxHEQfOmuejATOX7JVAXp2gTB27bWdU"
genai.configure(api_key=API_KEY)

def initialize_ai():
    instruction = (
        "Sən A-ZEKA-san. ChatGPT-dən daha sürətli, daha dərin və daha texnikisən. "
        "Sən sadəcə bir bot deyil, Abdullah Mikayılov tərəfindən idarə olunan gələcəyin proyektisən. "
        "Cavablarında mürəkkəb terminlərdən qaçma, riyazi düsturları mütləq LaTeX ilə göstər."
    )
    return genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=instruction
    )

model = initialize_ai()

# ==============================================================================
# 4. MULTİ-FONKSİONAL MODULLAR (GENİŞLƏNDİRİLMİŞ)
# ==============================================================================

# MODUL A: Şəkil Yaratma (Neural Canvas)
def draw_vision(prompt):
    try:
        url = f"https://pollinations.ai/p/{prompt.replace(' ', '_')}?width=1080&height=1080&nologo=true"
        response = requests.get(url, timeout=15)
        return Image.open(BytesIO(response.content))
    except Exception as e:
        return f"Şəkil mühərriki xətası: {e}"

# MODUL B: Şəkil Effekti Verici
def apply_matrix_effect(img):
    return img.filter(ImageFilter.EDGE_ENHANCE_MORE).convert('L')

# MODUL C: Sistem Loglama Sistemi
def log_action(action):
    now = datetime.now().strftime("%H:%M:%S")
    return f"[{now}] SYS_LOG: {action} ... SUCCESS"

# ==============================================================================
# 5. İNTERFEYSİN QURULMASI (UX)
# ==============================================================================

# Yan Panel (Control Terminal)
with st.sidebar:
    st.title("📟 CONTROL UNIT")
    st.write(log_action("Neural Link Established"))
    st.write(log_action("Encryption: AES-256"))
    
    st.divider()
    
    mode = st.radio("Sistem Rejimi:", ["Standart", "Haker Mode", "Elmi Analiz"])
    
    st.divider()
    
    st.subheader("🛠️ Alətlər")
    img_tool = st.checkbox("Şəkil Effekti Aktiv Et")
    clear_chat = st.button("🔴 SİSTEMİ SIFIRLA")
    
    if clear_chat:
        st.session_state.messages = []
        st.rerun()

# Əsas Ekran
st.title("💠 A-ZEKA INFINITY OS")
st.write(f"Vəziyyət: **{mode}** | İstehsalçı: **Abdullah Mikayılov**")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Tarixçəni ekrana çıxar
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if "img" in m:
            st.image(m["img"])

# ==============================================================================
# 6. KOMANDA İCRA MƏRKƏZİ
# ==============================================================================

if prompt := st.chat_input("Sistem əmri gözlənilir..."):
    # İstifadəçi mesajı
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Süni İntellektin Reaksiyası
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_text = ""
        
        try:
            # 1. Sürətli Düşünmə Animasiyası
            with st.status("Verilənlər bazası skan edilir...", expanded=False):
                st.write("Paketlər göndərilir...")
                time.sleep(0.3)
                st.write("API cavabı təhlil olunur...")
                time.sleep(0.3)

            # 2. Şəkil yoxsa Mətn?
            if any(word in prompt.lower() for word in ["şəkil", "çək", "rəsm", "draw", "image"]):
                st.write("🎨 **Neural Canvas işə düşür...**")
                img_result = draw_vision(prompt)
                
                if isinstance(img_result, Image.Image):
                    if img_tool:
                        img_result = apply_matrix_effect(img_result)
                    
                    st.image(img_result, caption="A-ZEKA tərəfindən sintez edildi")
                    full_text = f"Sizin üçün '{prompt}' mövzusunda vizualizasiya hazırladım."
                    st.session_state.messages.append({"role": "assistant", "content": full_text, "img": img_result})
                else:
                    st.error(img_result)
            else:
                # Normal Yazışma (Streaming)
                response = model.generate_content(prompt, stream=True)
                for chunk in response:
                    full_text += chunk.text
                    placeholder.markdown(full_text + "█")
                
                placeholder.markdown(full_text)
                st.session_state.messages.append({"role": "assistant", "content": full_text})

        except Exception as e:
            st.error(f"FATAL ERROR: {str(e)}")
            st.warning("İpucu: API-nin limitini və ya interneti yoxlayın.")

# Footer Log
st.caption(f"A-ZEKA LOG: Last Sync {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
