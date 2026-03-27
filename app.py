import streamlit as st
import google.generativeai as genai

# 1. SƏHİFƏ VƏ VİZUAL EFFEKTLƏR
st.set_page_config(page_title="A-ZEKA Ultra Pro", page_icon="🚀", layout="wide")

# Müasir UI/UX Dizaynı
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stChatInput { border-radius: 25px !important; border: 1px solid #3d5afe !important; }
    .stChatMessage { border-radius: 15px; border-left: 5px solid #3d5afe; background-color: #1e1e1e; color: white; }
    </style>
""", unsafe_allow_html=True)

# 2. API KONFİQURASİYASI
API_KEY = "AIzaSyByvxHEQfOmuejATOX7JVAXp2gTB27bWdU"
genai.configure(api_key=API_KEY)

# 3. MÜHƏRRİK VƏ AYARLAR
# Sürət və dəqiqlik balansı üçün parametrlər
generation_config = {
    "temperature": 0.6,
    "top_p": 0.9,
    "top_k": 40,
    "max_output_tokens": 4096,
}

# Sistem təlimatı (Şəxsiyyət qazandırırıq)
system_prompt = (
    "Sən A-ZEKA adlı üstün süni intellektsən. "
    "Riyazi düsturları həmişə LaTeX formatında (məsələn, $E=mc^2$) yaz. "
    "Proqramlaşdırma kodlarını müvafiq dil bloklarında göstər. "
    "Azərbaycan dilində qüsursuz, professional və intellektual cavablar ver."
)

@st.cache_resource
def load_model():
    try:
        # Ən yeni model adı bəzən 'gemini-2.0-flash-exp' və ya 'gemini-1.5-flash' olur. 
        # Sənin regionunda ən stabil olanı 1.5-flash-dır.
        return genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
            system_instruction=system_prompt
        )
    except Exception:
        return genai.GenerativeModel("gemini-pro")

model = load_model()

# 4. YADDAŞ (Söhbət Tarixçəsi)
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- İNTERFEYS ---
st.title("🚀 A-ZEKA Ultra Pro")
st.caption("AI Engine: Gemini 1.5 Flash | Status: Active 🟢")

# Yan Panel (Sidebar)
with st.sidebar:
    st.header("⚙️ Ayarlar")
    if st.button("🗑️ Tarixçəni Təmizlə", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.info("Bu proqram ən mürəkkəb elmi və texniki tapşırıqlar üçün optimallaşdırılıb.")

# Əvvəlki mesajları göstər
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. SUAL-CAVAB VƏ STREAMING (CANLI YAZI)
if prompt := st.chat_input("Sualınızı bura daxil edin..."):
    # İstifadəçi mesajı
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Süni İntellektin cavabı
    with st.chat_message("assistant"):
        message_placeholder = st.empty() # Canlı effekt üçün yer ayırırıq
        full_response = ""
        
        try:
            # stream=True sayəsində model cavabı hissə-hissə göndərir
            response = model.generate_content(prompt, stream=True)
            
            for chunk in response:
                full_response += chunk.text
                # Ekranda yazılma effekti yaradırıq
                message_placeholder.markdown(full_response + "▌")
            
            # Tam cavabı yadda saxla
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Xəta baş verdi: {str(e)}")
