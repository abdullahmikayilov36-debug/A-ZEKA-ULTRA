import streamlit as st
import google.generativeai as genai
import time
import requests
from io import BytesIO
from PIL import Image

# ==========================================
# 1. ULTRA FUTURİSTİK NEON DİZAYN (CSS)
# ==========================================
st.set_page_config(page_title="A-ZEKA Genesis", page_icon="💠", layout="wide")

st.markdown("""
<style>
    /* Ana Fon və Cyberpunk rəngləri */
    .stApp {
        background: radial-gradient(circle, #0d1117 0%, #010409 100%);
        color: #e6edf3;
    }
    /* Çat qutularının dizaynı */
    .stChatMessage {
        border: 1px solid #30363d;
        border-radius: 20px !important;
        background: rgba(22, 27, 34, 0.8) !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    /* Neon effektli giriş sahəsi */
    .stChatInput {
        border-radius: 30px !important;
        border: 1px solid #58a6ff !important;
        box-shadow: 0 0 10px #58a6ff;
    }
    /* Başlıq stili */
    h1 {
        color: #58a6ff;
        text-shadow: 0 0 20px #58a6ff;
        font-family: 'Courier New', Courier, monospace;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. API VƏ MODELİN QURULMASI
# ==========================================
# Sənin aldığın yeni açarı bura yapışdır:
API_KEY = "AIzaSyByvxHEQfOmuejATOX7JVAXp2gTB27bWdU"
genai.configure(api_key=API_KEY)

# A-ZEKA-nın Beyin Təlimatı
sys_instruct = """
Sən A-ZEKA-san. Dünyanın ən inkişaf etmiş AI sistemisən.
1. Əgər istifadəçi "şəkil çək", "şəkil yarat" kimi əmrlər versə, cavabının əvvəlinə mütləq '[DRAW]' sözünü yaz.
2. Cavablarında həmişə professional və haker stilində danış.
3. Riyazi düsturları LaTeX formatında yaz.
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=sys_instruct
)

# ==========================================
# 3. ŞƏKİL YARATMA MÜHƏRRİKİ (IMAGE GEN)
# ==========================================
def generate_ai_image(prompt):
    """Pulsuz və sürətli şəkil yaratma mühərriki (Pollinations/Unsplash AI)"""
    try:
        # Şəkli yaratmaq üçün sorğu
        image_url = f"https://pollinations.ai/p/{prompt.replace(' ', '_')}?width=1024&height=1024&seed=42"
        response = requests.get(image_url)
        return Image.open(BytesIO(response.content))
    except:
        return None

# ==========================================
# 4. YADDAŞ VƏ İNTERFEYS
# ==========================================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("💠 A-ZEKA GENESIS")
st.caption("Status: System Online | Neural Link: Stable")

# Yan Menyu (Sidebar)
with st.sidebar:
    st.header("⚙️ Sistem Ayarları")
    if st.button("🗑️ Terminalı Sıfırla"):
        st.session_state.chat_history = []
        st.rerun()
    st.divider()
    st.info("A-ZEKA həm danışır, həm də şəkil yaradır.")

# Tarixçəni göstər
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "image" in msg:
            st.image(msg["image"])

# ==========================================
# 5. ƏMRLƏRİN İCRA EDİLMƏSİ
# ==========================================
if prompt := st.chat_input("Komanda daxil edin..."):
    # İstifadəçinin mesajı
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # A-ZEKA-nın cavabı
    with st.chat_message("assistant"):
        with st.spinner("Analiz edilir..."):
            try:
                response = model.generate_content(prompt)
                full_text = response.text
                
                # ŞƏKİL ÇƏKMƏ ŞƏRTİ YOXLA
                if "[DRAW]" in full_text.upper() or "şəkil" in prompt.lower():
                    st.write("🎨 Şəkil generatsiya olunur...")
                    generated_img = generate_ai_image(prompt)
                    if generated_img:
                        st.image(generated_img, caption="A-ZEKA tərəfindən yaradıldı")
                        st.session_state.chat_history.append({
                            "role": "assistant", 
                            "content": full_text.replace("[DRAW]", ""), 
                            "image": generated_img
                        })
                    else:
                        st.error("Şəkil mühərrikində xəta!")
                else:
                    st.markdown(full_text)
                    st.session_state.chat_history.append({"role": "assistant", "content": full_text})
            
            except Exception as e:
                st.error(f"Sistem xətası: {e}")
