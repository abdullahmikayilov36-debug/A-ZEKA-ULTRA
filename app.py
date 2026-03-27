import streamlit as st
import google.generativeai as genai

# 1. SƏHİFƏ AYARLARI
st.set_page_config(page_title="A-ZEKA Ultra Fast", page_icon="⚡")

# 2. API QOŞULMASI
API_KEY = "AIzaSyByvxHEQfOmuejATOX7JVAXp2gTB27bWdU"
genai.configure(api_key=API_KEY)

# 3. MODEL AYARLARI (Sürət üçün optimizasiya edilib)
generation_config = {
  "temperature": 0.5, # Daha sürətli və dəqiq cavab üçün
  "top_p": 0.9,
  "top_k": 32,
  "max_output_tokens": 2048,
}

# Ən sürətli stabil model: gemini-1.5-flash
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config
)

# 4. YADDAŞ
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- İNTERFEYS ---
st.title("⚡ A-ZEKA Sürətli Versiya")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Sualınızı bura yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty() # Canlı yazı üçün yer açırıq
        full_response = ""
        
        try:
            # stream=True yazaraq cavabı hissə-hissə alırıq (Çox sürətli görünür)
            response = model.generate_content(prompt, stream=True)
            
            for chunk in response:
                full_response += chunk.text
                placeholder.markdown(full_response + "▌") # Yazılma effekti
            
            placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Xəta: {e}")
