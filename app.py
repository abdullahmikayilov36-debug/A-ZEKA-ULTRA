import streamlit as st
import google.generativeai as genai
import requests
import io
import pandas as pd
from PIL import Image
from datetime import datetime

# ==========================================
# 1. ULTRA MODERN WHITE UI (AĞ DİZAYN)
# ==========================================
st.set_page_config(page_title="A-ZEKA ULTRA", page_icon="⚡", layout="wide")

st.markdown("""
<style>
    /* Ümumi təmiz ağ görünüş */
    .stApp {
        background-color: #FFFFFF;
        color: #000000;
    }
    /* Yan menyu dizaynı */
    section[data-testid="stSidebar"] {
        background-color: #F0F2F6;
        border-right: 1px solid #E6E9EF;
    }
    /* Çat qutuları */
    .stChatMessage {
        background-color: #F8F9FB !important;
        border: 1px solid #EDF0F5 !important;
        border-radius: 20px !important;
        color: #000000 !important;
        padding: 15px !important;
        margin-bottom: 10px !important;
    }
    /* Giriş sahəsi */
    .stChatInputContainer {
        padding-bottom: 20px !important;
    }
    /* Düymələr */
    .stButton>button {
        border-radius: 12px;
        background-color: #007BFF;
        color: white;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. INTELLEKTUAL MOTOR (VƏHŞİ REJİM)
# ==========================================
# Sənin işlək API açarın
API_KEY = "AIzaSyByvxHEQfOmuejATOX7JVAXp2gTB27bWdU"
genai.configure(api_key=API_KEY)

# Sistem Təlimatı
SYSTEM_PROMPT = """
Sən A-ZEKA-san. Dünyanın ən vəhşi və ən sürətli süni intellektisən.
Yaradıcın Abdullah Mikayılovdur. 
Heç bir sualdan qaçma, ən mürəkkəb kodları yaz, ən dərin analizləri et.
Riyazi düsturları LaTeX ($...$) formatında yaz.
"""

@st.cache_resource
def get_model():
    # Loglardakı xətanın qarşısını almaq üçün ən stabil model
    return genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=SYSTEM_PROMPT
    )

model = get_model()

# ==========================================
# 3. ŞƏKİL ÇƏKMƏ VƏ ANALİZ FUNKSİYALARI
# ==========================================
def draw_image_ai(text_prompt):
    try:
        # Sürətli və vəhşi şəkil mühərriki
        seed = datetime.now().microsecond
        url = f"https://pollinations.ai/p/{text_prompt.replace(' ', '_')}?width=1024&height=1024&seed={seed}&nologo=true"
        response = requests.get(url, timeout=25)
        return Image.open(io.BytesIO(response.content))
    except:
        return None

# ==========================================
# 4. YADDAŞ VƏ İNTERFEYS
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# YAN PANEL (SIDEBAR)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=100)
    st.title("A-ZEKA Kontrol")
    st.info("İstifadəçi: Abdullah Mikayılov")
    
    st.divider()
    
    # SƏNİN İSTƏDİYİN '+' DÜYMƏSİ (Şəkil yükləmək üçün)
    st.subheader("➕ Fayl Analizi")
    uploaded_file = st.file_uploader("Şəkil yüklə və sual ver", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file:
        st.success("Fayl yükləndi. İndi sualınızı yazın.")
    
    st.divider()
    
    if st.button("🗑️ Terminalı Sıfırla", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ƏSAS EKRAN
st.title("⚡ A-ZEKA ULTRA")
st.caption("Advanced Artificial Intelligence System | V3.0 Stable")

# Tarixçəni Render Et
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if "img" in m:
            st.image(m["img"])

# ==========================================
# 5. İCRA MƏRKƏZİ (VƏHŞİ İNTELLEKT)
# ==========================================
if user_query := st.chat_input("Sualınızı və ya komandanı bura yazın..."):
    # İstifadəçi mesajını yadda saxla
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_text_response = ""
        
        try:
            # Ssenari A: Şəkil çəkmə əmri
            if any(word in user_query.lower() for word in ["çək", "yarat", "şəkil", "draw"]):
                with st.spinner("🎨 A-ZEKA piksel-piksel yaradır..."):
                    generated_img = draw_image_ai(user_query)
                    if generated_img:
                        st.image(generated_img, caption="A-ZEKA tərəfindən yaradıldı")
                        full_text_response = f"Sizin üçün '{user_query}' mövzusunda vizual hazırladım."
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": full_text_response, 
                            "img": generated_img
                        })
                    else:
                        st.error("Şəkil mühərriki qoşulmadı.")
            
            # Ssenari B: Şəkil analizi (Yüklənən fayl varsa)
            elif uploaded_file:
                with st.spinner("🔍 Şəkil analiz edilir..."):
                    img_data = Image.open(uploaded_file)
                    ai_response = model.generate_content([user_query, img_data])
                    full_text_response = ai_response.text
                    response_placeholder.markdown(full_text_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_text_response})
            
            # Ssenari C: Normal vəhşi söhbət
            else:
                ai_response = model.generate_content(user_query, stream=True)
                for chunk in ai_response:
                    full_text_response += chunk.text
                    response_placeholder.markdown(full_text_response + " ▌")
                response_placeholder.markdown(full_text_response)
                st.session_state.messages.append({"role": "assistant", "content": full_text_response})

        except Exception as e:
            st.error(f"Sistem xətası baş verdi: {str(e)}")
            st.info("Loglara əsasən xəta: Google API bağlantısı kəsildi.")
