import streamlit as st
import google.generativeai as genai

# Səhifə dizaynı ayarları
st.set_page_config(page_title="A-ZEKA Ultra", page_icon="🤖", layout="wide")

# API Ayarı (Öz API açarını bura yaz)
genai.configure(api_key="SENIN_API_ACARIN")

# Modelin "Beyin" ayarları (Ən mürəkkəb suallar üçün Pro model)
generation_config = {
  "temperature": 0.7, # Yaradıcılıq və məntiq balansı
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192, # Uzun və ətraflı cavablar üçün
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    system_instruction="Sən dünyanın ən güclü və dəqiq intellektisən. Mürəkkəb elmi, texniki və tarixi suallara detallı, məntiqli və aydın cavablar verirsən."
)

# Tarixçəni (Yaddaşı) idarə etmək
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# --- Dizayn və İnterfeys ---
st.title("🚀 A-ZEKA Ultra Pro")
st.markdown("---")

# Yan menyu (Tarixçəni silmək və tənzimləmələr üçün)
with st.sidebar:
    st.header("⚙️ Ayarlar")
    if st.button("🗑️ Tarixçəni Təmizlə"):
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()
    st.info("Bu intellekt Gemini 1.5 Pro mühərriki ilə işləyir.")

# Mesajların ekranda görünməsi
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
