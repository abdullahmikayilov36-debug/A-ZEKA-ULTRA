import streamlit as st
import google.generativeai as genai
import pandas as pd
import time
import base64
from datetime import datetime
from PIL import Image
import io

# ==========================================
# 1. SİSTEM KONFİQURASİYASI VƏ DİZAYN (CSS)
# ==========================================
st.set_page_config(
    page_title="A-ZEKA Ultimate OS",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Xüsusi Pro Dizayn (Cyberpunk/Modern Style)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'JetBrains+Mono', monospace;
    }
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #ffffff;
    }
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px !important;
        backdrop-filter: blur(10px);
        margin-bottom: 15px;
    }
    .stChatInput {
        border-radius: 30px !important;
        background-color: #16213e !important;
    }
    .sidebar .sidebar-content {
        background-image: linear-gradient(#2e3440,#2e3440);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. API VƏ MODELİN QURULMASI
# ==========================================
# DİQQƏT: Yeni aldığın açarı bura yaz!
API_KEY = "BURA_YENİ_AÇARI_YAZ" 

if API_KEY != "BURA_YENİ_AÇARI_YAZ":
    genai.configure(api_key=API_KEY)
else:
    st.warning("⚠️ Zəhmət olmasa API açarını koda əlavə edin!")

# Model Parametrləri
generation_config = {
    "temperature": 0.8,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 16384, # Maksimum uzunluq
}

# Sistem Təlimatı (A-ZEKA-nın Beyni)
system_prompt = """
Sən A-ZEKA-san. Dünyanın ən qabaqcıl süni intellekt sistemisən. 
Funksiyaların:
1. Elmi tədqiqat və dərin analiz.
2. Proqramlaşdırma (Python, JS, C++, SQL).
3. Riyazi modelləşdirmə (LaTeX istifadə edərək).
4. Tarixi və mədəni biliklər.
Həmişə professional, dəqiq və səmimi cavablar ver.
"""

@st.cache_resource
def init_models():
    # Multimodal (Həm şəkil, həm mətn) model
    return genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction=system_prompt
    )

try:
    model = init_models()
except:
    st.error("Sistem qoşulma xətası!")

# ==========================================
# 3. MƏLUMAT BAZASI VƏ YADDAŞ (DATABASE)
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = datetime.now().strftime("%Y%m%d%H%M%S")
if "metrics" not in st.session_state:
    st.session_state.metrics = {"tokens": 0, "requests": 0}

# ==========================================
# 4. YAN MENYU (SİSTEM PANELİ)
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712109.png", width=80)
    st.title("A-ZEKA Control Center")
    st.write(f"📅 Tarix: {datetime.now().strftime('%d.%m.%Y')}")
    st.write(f"🆔 Session: {st.session_state.session_id}")
    
    st.divider()
    
    st.subheader("💾 Fayl Analizi")
    uploaded_file = st.file_uploader("Şəkil və ya sənəd yükləyin", type=['png', 'jpg', 'jpeg', 'pdf'])
    
    st.divider()
    
    st.subheader("📊 Sistem Metrikləri")
    col1, col2 = st.columns(2)
    col1.metric("Sorğular", st.session_state.metrics["requests"])
    col2.metric("Status", "Online", delta="Stable")
    
    if st.button("🗑️ Terminalı Təmizlə", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ==========================================
# 5. ƏSAS ÇAT FUNKSİONALLIĞI
# ==========================================
st.title("💠 A-ZEKA: Universal İntellekt")
st.caption("Advanced Neural Network Interface v3.5.0")

# Mesaj Tarixçəsini Render Et
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Giriş Sahəsi
if prompt := st.chat_input("Sistemə sorğu daxil edin..."):
    # İstifadəçi mesajını yadda saxla
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Cavab Generatoru
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        # Proqres bar (Düşünmə simulyasiyası)
        progress_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.005) # Sürətli keçid
            progress_bar.progress(percent_complete + 1)
        progress_bar.empty()

        try:
            # Şəkil analizi yoxlanışı
            if uploaded_file:
                img = Image.open(uploaded_file)
                response = model.generate_content([prompt, img], stream=True)
            else:
                response = model.generate_content(prompt, stream=True)

            # Streaming Output
            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    placeholder.markdown(full_response + "▌")
            
            placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            st.session_state.metrics["requests"] += 1
            
        except Exception as e:
            st.error(f"⚠️ SİSTEM XƏTASI: {str(e)}")
            st.info("İpucu: API açarını və internet bağlantısını yoxlayın.")

# ==========================================
# 6. SİSTEM LOGLARI (FOOTER)
# ==========================================
st.divider()
st.markdown(f"<p style='text-align: center; color: grey;'>A-ZEKA Core v3.5 | Developer: Abdullah Mikayılov | {datetime.now().year}</p>", unsafe_allow_html=True)
