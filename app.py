import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. SƏHİFƏ VƏ DİZAYN AYARLARI ---
st.set_page_config(page_title="A-ZEKA | Süni İntellekt", page_icon="⚡", layout="wide")

# Xüsusi CSS dizaynı (Koda peşəkar görünüş qatır)
st.markdown("""
<style>
    .stChatMessage {border-radius: 10px; padding: 15px; margin-bottom: 10px;}
    .stChatInput {border-radius: 15px !important;}
</style>
""", unsafe_allow_html=True)

# --- 2. API TƏNZİMLƏMƏLƏRİ ---
API_KEY = "AIzaSyCIwmGxUyFH9IbLd1yF_LuUPK11rCtkuss"
genai.configure(api_key=API_KEY)

# A-ZEKA-nın Şəxsiyyəti və Təlimatları (LaTeX və riyaziyyat dəstəyi ilə)
sys_instruct = """
Sən A-ZEKA adlı çox inkişaf etmiş, xüsusi bir süni intellektsən. 
Əsas vəzifən istifadəçiyə ən mürəkkəb elmi, texniki, proqramlaşdırma və riyazi suallarda kömək etməkdir.
Riyazi düsturları və tənlikləri həmişə LaTeX formatında yaz ki, ekranda vizual olaraq qüsursuz görünsün.
Eyni zamanda göndərilən şəkilləri detallı analiz edə bilirsən. Qısa, dəqiq və professional cavablar ver.
"""

# Modeli seçirik (Həm mətn, həm şəkil üçün ən ideal olan gemini-1.5-flash-dır, xəta verməməsi üçün try-except qurduq)
try:
    model = genai.GenerativeModel(
        model_name="models/gemini-1.5-flash", 
        system_instruction=sys_instruct
    )
except Exception as e:
    st.error(f"Model yüklənmədi. Səbəb: {e}")

# --- 3. YADDAŞ (TARİXÇƏ) İDARƏETMƏSİ ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- 4. YAN MENYU (SIDEBAR) VƏ AYARLAR ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Google_Gemini_logo.svg/512px-Google_Gemini_logo.svg.png", width=100)
    st.title("⚙️ A-ZEKA İdarə Paneli")
    st.markdown("Dünyanın ən güclü AI mühərriklərindən biri ilə təchiz edilib.")
    
    st.divider()
    
    # Tarixçəni silmək düyməsi
    if st.button("🗑️ Bütün Söhbəti Sil", use_container_width=True):
        st.session_state.chat_history = []
        st.success("Tarixçə təmizləndi!")
        st.rerun()
        
    st.divider()
    
    # Şəkil yükləmək üçün funksiya (Multimodal dəstək)
    st.markdown("### 📷 Şəkil Analizi")
    uploaded_file = st.file_uploader("Sualınla bağlı şəkil yüklə", type=["png", "jpg", "jpeg"])

# --- 5. ƏSAS EKRAN VƏ SÖHBƏT İNTERFEYSİ ---
st.title("⚡ A-ZEKA - Universal İntellekt")
st.caption("Riyaziyyat, Kodlaşdırma, Şəkil Analizi və daha nələr...")

# Yaddaşdakı əvvəlki mesajları ekrana çıxarırıq
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 6. SUAL GÖNDƏRMƏ VƏ CAVAB ALMA ---
if user_input := st.chat_input("Sualınızı və ya tapşırığınızı daxil edin..."):
    
    # İstifadəçinin mesajını ekrana yaz və yaddaşa sal
    st.chat_message("user").markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    with st.chat_message("assistant"):
        with st.spinner("A-ZEKA məlumatları işləyir..."):
            try:
                # Əgər istifadəçi şəkil yükləyibsə, həm şəkil, həm də mətni göndəririk
                if uploaded_file is not None:
                    img = Image.open(uploaded_file)
                    response = model.generate_content([user_input, img])
                # Yalnız mətn varsa
                else:
                    response = model.generate_content(user_input)
                
                # Cavabı ekrana yaz və yaddaşa sal
                st.markdown(response.text)
                st.session_state.chat_history.append({"role": "assistant", "content": response.text})
                
            except Exception as e:
                st.error(f"Sistem Xətası: {e}\nZəhmət olmasa biraz sonra təkrar yoxlayın və ya API açarını yoxlayın.")
