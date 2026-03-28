import streamlit as st
import google.generativeai as genai
import requests
import pandas as pd
import time
import io
from PIL import Image, ImageEnhance, ImageFilter
from datetime import datetime

# ==============================================================================
# 1. ULTRA MODERN VƏ TƏMİZ DİZAYN (WHITE MODE)
# ==============================================================================
st.set_page_config(page_title="A-ZEKA PRO MAX", page_icon="🤖", layout="wide")

# Sənin istədiyin Ağ Dizayn və Professional Görünüş
st.markdown("""
<style>
    /* Ana Fon - Təmiz Ağ */
    .stApp {
        background-color: #FFFFFF;
        color: #1A1A1A;
    }
    
    /* Yan Menyu */
    [data-testid="stSidebar"] {
        background-color: #F8F9FA;
        border-right: 1px solid #E0E0E0;
    }
    
    /* Mesaj qutuları */
    .stChatMessage {
        border-radius: 20px !important;
        padding: 20px !important;
        margin-bottom: 15px !important;
        border: 1px solid #F0F0F0 !important;
    }
    
    /* İstifadəçi mesajı */
    [data-testid="stChatMessageUser"] {
        background-color: #F0F2F6 !important;
    }
    
    /* AI mesajı */
    [data-testid="stChatMessageAssistant"] {
        background-color: #FFFFFF !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }

    /* Giriş sahəsi (Chat Input) */
    .stChatInput {
        border-radius: 15px !important;
        border: 1px solid #DEDEDE !important;
    }

    /* Düymələr */
    .stButton>button {
        border-radius: 10px;
        background-color: #007BFF;
        color: white;
        border: none;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. INTELLEKTUAL MOTOR (GEMINI CORE)
# ==============================================================================
# API Açarını bura daxil edirik
API_KEY = "AIzaSyByvxHEQfOmuejATOX7JVAXp2gTB27bWdU"
genai.configure(api_key=API_KEY)

# A-ZEKA Təlimatları
instruction = (
    "Sən A-ZEKA-san. Dünyanın ən güclü və 'vəhşi' intellektisən. "
    "Məqsədin Abdullah Mikayılova ən mürəkkəb elmi, texniki və bədii məsələlərdə kömək etməkdir. "
    "Riyazi düsturları mütləq LaTeX ($...$) ilə yaz. Proqramlaşdırma kodlarını bloklarda göstər."
)

@st.cache_resource
def load_system():
    # Bu model həm mətni, həm şəkilləri eyni anda analiz edə bilir
    return genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=instruction
    )

model = load_system()

# ==============================================================================
# 3. MULTİMODAL FUNKSİYALAR (ŞƏKİL ÇƏKMƏ VƏ ANALİZ)
# ==============================================================================

# Şəkil Çəkmə Mühərriki
def paint_art(prompt):
    try:
        url = f"https://pollinations.ai/p/{prompt.replace(' ', '_')}?width=1024&height=1024&nologo=true"
        r = requests.get(url, timeout=20)
        return Image.open(io.BytesIO(r.content))
    except:
        return None

# Şəkil Effektləri (Editləmək üçün)
def process_image(img, mode):
    if mode == "Qara-Ağ":
        return img.convert("L")
    elif mode == "Kəskin":
        return img.filter(ImageFilter.SHARPEN)
    elif mode == "Parlaq":
        enhancer = ImageEnhance.Brightness(img)
        return enhancer.enhance(1.5)
    return img

# ==============================================================================
# 4. YADDAŞ VƏ SESSİYA İDARƏETMƏSİ
# ==============================================================================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "metrics" not in st.session_state:
    st.session_state.metrics = {"queries": 0, "images": 0}

# ==============================================================================
# 5. İNTERFEYS (UI) - SOL PANEL
# ==============================================================================
with st.sidebar:
    st.title("⚙️ A-ZEKA Panel")
    st.write(f"Salam, **Abdullah**!")
    
    # ŞƏKİL YÜKLƏMƏK ÜÇÜN O '+' DÜYMƏSİ FUNKSİYASI
    st.subheader("➕ Fayl Əlavə Et")
    uploaded_file = st.file_uploader("Analiz üçün şəkil seçin", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file:
        st.image(uploaded_file, caption="Yüklənən fayl", use_container_width=True)
    
    st.divider()
    
    # Alətlər
    st.subheader("🛠️ İntellekt Alətləri")
    tool_mode = st.selectbox("Rejim seçin:", ["Söhbət", "Şəkil Yaradıcısı", "Kod Analizi"])
    
    if st.button("🗑️ Tarixçəni Təmizlə", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

# ==============================================================================
# 6. ƏSAS SÖHBƏT MƏKANI
# ==============================================================================
st.title("🤖 A-ZEKA PRO MAX")
st.info("Sistem online və vəhşi rejimdədir. Sualınızı və ya şəkil komandanızı daxil edin.")

# Mesajları ekranda göstər
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "img" in msg:
            st.image(msg["img"])

# GİRİŞ VƏ MÜHƏRRİKİN İŞƏ DÜŞMƏSİ
if prompt := st.chat_input("Buraya yazın..."):
    # İstifadəçi mesajını qeyd et
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Süni İntellektin reaksiyası
    with st.chat_message("assistant"):
        res_container = st.empty()
        full_text = ""
        
        try:
            # Ssenari 1: Şəkil çəkmək istəyirsə
            if any(x in prompt.lower() for x in ["çək", "yarat", "şəkil", "draw", "paint"]):
                with st.spinner("🎨 A-ZEKA şəkli xəyal edir..."):
                    art = paint_art(prompt)
                    if art:
                        st.image(art, caption="A-ZEKA Genesis Engine")
                        full_text = f"İstəyinizə uyğun olaraq '{prompt}' şəklini hazırladım."
                        st.session_state.chat_history.append({
                            "role": "assistant", 
                            "content": full_text, 
                            "img": art
                        })
                        st.session_state.metrics["images"] += 1
                    else:
                        st.error("Şəkil mühərriki müvəqqəti olaraq dayandı.")
            
            # Ssenari 2: Şəkil yüklənibsə və analiz istəyirsə
            elif uploaded_file:
                with st.spinner("🔍 Şəkil analiz olunur..."):
                    img_data = Image.open(uploaded_file)
                    response = model.generate_content([prompt, img_data])
                    full_text = response.text
                    res_container.markdown(full_text)
                    st.session_state.chat_history.append({"role": "assistant", "content": full_text})

            # Ssenari 3: Normal vəhşi intellekt cavabı
            else:
                response = model.generate_content(prompt, stream=True)
                for chunk in response:
                    full_text += chunk.text
                    res_container.markdown(full_text + " ▌")
                res_container.markdown(full_text)
                st.session_state.chat_history.append({"role": "assistant", "content": full_text})
                st.session_state.metrics["queries"] += 1

        except Exception as e:
            st.error(f"⚠️ Kritik Xəta: {e}")
            st.info("Log: API açarını və ya 'requirements.txt' faylını yoxlayın.")

# ==============================================================================
# 7. FOOTER (SİSTEM STATUSU)
# ==============================================================================
st.divider()
c1, c2, c3 = st.columns(3)
c1.write(f"🆔 Session: {datetime.now().strftime('%H%M%S')}")
c2.write(f"📊 Sorğular: {st.session_state.metrics['queries']}")
c3.write(f"⚡ Motor: Gemini 1.5 Flash")
