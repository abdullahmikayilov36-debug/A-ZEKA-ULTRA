import streamlit as st
import google.generativeai as genai

# 1. SƏHİFƏ AYARLARI
st.set_page_config(page_title="A-ZEKA Ultra", page_icon="🤖")

# 2. API QOŞULMASI
# BURAYA YENİ ALDIĞIN API AÇARINI YAPIŞDIR
API_KEY = "YENİ_ALDIĞIN_ACARI_BURA_YAZ" 
genai.configure(api_key=API_KEY)

# 3. MODEL AYARLARI (Ən sürətli və stabil versiya)
@st.cache_resource
def load_model():
    return genai.GenerativeModel('gemini-1.5-flash')

model = load_model()

# 4. YADDAŞ (Söhbət Tarixçəsi)
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- İNTERFEYS ---
st.title("🚀 A-ZEKA Ultra")
st.markdown("---")

# Tarixçəni göstər
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Sual daxil etmə (STREAMING DESTEKLİ)
if prompt := st.chat_input("Mənə sual ver..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        try:
            # stream=True sayəsində cavab dərhal yazılmağa başlayır
            response = model.generate_content(prompt, stream=True)
            for chunk in response:
                full_response += chunk.text
                placeholder.markdown(full_response + "▌")
            
            placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Xəta: {e}")
            st.info("Əgər 'Expired' xətası alırsansa, Google AI Studio-dan yeni açar alıb koda yapışdır.")
