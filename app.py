import streamlit as st
import google.generativeai as genai

# 1. SƏHİFƏ DİZAYNI VƏ AYARLARI
st.set_page_config(page_title="A-ZEKA Ultra", page_icon="🤖", layout="wide")

# Xüsusi Görünüş (Daha müasir dizayn)
st.markdown("""
<style>
    .stChatInput {border-radius: 20px !important;}
    .stChatMessage {border-radius: 15px; margin-bottom: 10px;}
</style>
""", unsafe_allow_html=True)

# 2. YENİ API AÇARININ QOŞULMASI
API_KEY = "AIzaSyByvxHEQfOmuejATOX7JVAXp2gTB27bWdU"
genai.configure(api_key=API_KEY)

# 3. MODELİN TƏYİNİ (Ən son Gemini 3 Flash modeli)
# Bu model Google AI Studio-da gördüyün ən yeni mühərrikdir
try:
    model = genai.GenerativeModel(
        model_name="gemini-3-flash-preview",
        system_instruction="Sən A-ZEKA-san. Dünyanın ən mürəkkəb suallarına dəqiq, məntiqli və professional cavablar verən üstün bir intellektsən."
    )
except Exception as e:
    # Əgər 3-Flash hələ aktiv deyilsə, ehtiyat olaraq 1.5-flash-a keçir
    model = genai.GenerativeModel("gemini-1.5-flash")

# 4. YADDAŞ (Söhbəti xatırlamaq üçün)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- İNTERFEYS ---
st.title("🚀 A-ZEKA Ultra Pro")
st.subheader("Güclü, Dəqiq və Sürətli")

# Yan Menyu
with st.sidebar:
    st.header("⚙️ Ayarlar")
    if st.button("🗑️ Tarixçəni Sil", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()
    st.info("Bu sistem ən son Gemini 3 texnologiyası ilə təchiz olunub.")

# Mesajları Ekranda Göstər
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Sual Daxil Etmə Sahəsi
if prompt := st.chat_input("Mürəkkəb sualınızı bura yazın..."):
    # İstifadəçi mesajını göstər
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.chat_history.append({"role": "user", "content": prompt})

    # Cavab Alma
    with st.chat_message("assistant"):
        with st.spinner("A-ZEKA təhlil edir..."):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.chat_history.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Xəta baş verdi: {e}")
