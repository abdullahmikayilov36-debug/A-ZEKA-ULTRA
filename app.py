import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. SƏHİFƏ VƏ DİZAYN ---
st.set_page_config(page_title="A-ZEKA | Süni İntellekt", page_icon="⚡", layout="wide")

st.markdown("""
<style>
    .stChatMessage {border-radius: 10px; padding: 15px; margin-bottom: 10px;}
    .stChatInput {border-radius: 15px !important;}
</style>
""", unsafe_allow_html=True)

# --- 2. API TƏNZİMLƏMƏLƏRİ ---
API_KEY = "AIzaSyCIwmGxUyFH9IbLd1yF_LuUPK11rCtkuss"
genai.configure(api_key=API_KEY)

# --- 3. AVTOMATİK MODEL SEÇİCİ (404 Xətasının Həlli) ---
@st.cache_resource
def get_best_model():
    try:
        # Sənin açarının icazəsi olan bütün modelləri tapırıq
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Əgər siyahıda 1.5-flash varsa onu, yoxdursa pro versiyanı, heç biri yoxdursa icazə verilən ilk modeli seç
        if "models/gemini-1.5-flash" in available_models:
            return "models/gemini-1.5-flash"
        elif "models/gemini-pro" in available_models:
            return "models/gemini-pro"
        elif "gemini-1.5-flash" in available_models:
            return "gemini-1.5-flash"
        else:
            return available_models[0] # Nəyə icazə varsa onu məcbur seç
    except Exception:
        return "gemini-pro" # Ən son ehtiyat variant

# Təlimatlar
sys_instruct = """
Sən A-ZEKA adlı çox inkişaf etmiş, xüsusi bir süni intellektsən. 
Əsas vəzifən istifadəçiyə ən mürəkkəb elmi, texniki, proqramlaşdırma və riyazi suallarda kömək etməkdir.
Riyazi düsturları həmişə LaTeX formatında yaz. Qısa, dəqiq və professional cavablar ver.
"""

# Modeli işə salırıq
try:
    secilen_model_adi = get_best_model()
    model = genai.GenerativeModel(
        model_name=secilen_model_adi, 
        system_instruction=sys_instruct
    )
except Exception as e:
    st.error(f"Sistem xətası: {e}")

# --- 4. YADDAŞ ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- 5. YAN MENYU ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Google_Gemini_logo.svg/512px-Google_Gemini_logo.svg.png", width=100)
    st.title("⚙️ A-ZEKA Paneli")
    st.success(f"İstifadə olunan mühərrik: {secilen_model_adi}") # Ekranda hansı modelin işlədiyini göstərəcək
    st.divider()
    
    if st.button("🗑️ Bütün Söhbəti Sil", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()
        
    st.divider()
    st.markdown("### 📷 Şəkil Analizi")
    uploaded_file = st.file_uploader("Sualınla bağlı şəkil yüklə", type=["png", "jpg", "jpeg"])

# --- 6. ƏSAS EKRAN ---
st.title("⚡ A-ZEKA - Universal İntellekt")

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_input := st.chat_input("Sualınızı və ya tapşırığınızı daxil edin..."):
    st.chat_message("user").markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    with st.chat_message("assistant"):
        with st.spinner("A-ZEKA düşünür..."):
            try:
                if uploaded_file is not None:
                    img = Image.open(uploaded_file)
                    response = model.generate_content([user_input, img])
                else:
                    response = model.generate_content(user_input)
                
                st.markdown(response.text)
                st.session_state.chat_history.append({"role": "assistant", "content": response.text})
                
            except Exception as e:
                st.error(f"Sistem Xətası: {e}")
