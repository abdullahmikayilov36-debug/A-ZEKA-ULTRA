import streamlit as st
import google.generativeai as genai

# 1. Səhifənin vizual dizaynı
st.set_page_config(page_title="A-ZEKA Ultra", page_icon="🤖", layout="wide")

# 2. Sənin API açarın (Bura toxunma, artıq əlavə etdim)
genai.configure(api_key="AIzaSyCIwmGxUyFH9IbLd1yF_LuUPK11rCtkuss")

# 3. Modelin beynini tənzimləyirik
generation_config = {
  "temperature": 0.7,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
}

# 4. Ən stabil və sürətli model olan 'flash' versiyasını seçdik
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash", 
    generation_config=generation_config,
    system_instruction="Sən dünyanın ən güclü və dəqiq intellektisən. Adın A-ZEKA-dır. Mürəkkəb suallara aydın və dəqiq cavablar verirsən."
)

# 5. Söhbət tarixçəsini (Yaddaşı) başladırıq
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# --- EKRAN DİZAYNI ---
st.title("🚀 A-ZEKA Ultra Pro")
st.markdown("---")

# Yan menyu (Sidebar) - Tarixçəni silmək üçün
with st.sidebar:
    st.header("⚙️ Ayarlar")
    if st.button("🗑️ Tarixçəni Təmizlə"):
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()
    st.info("Bu sistem süni intellektin ən son versiyası ilə işləyir.")

# Əvvəlki mesajları ekranda göstər
for message in st.session_state.chat_session.history:
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# Sual daxil etmə sahəsi
if prompt := st.chat_input("Mürəkkəb sualınızı bura yazın..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.spinner("Düşünürəm..."):
        try:
            response = st.session_state.chat_session.send_message(prompt)
            with st.chat_message("assistant"):
                st.markdown(response.text)
        except Exception as e:
            st.error(f"Xəta baş verdi: {e}")
