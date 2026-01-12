import streamlit as st
from google import genai

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Chef AI: Masak Sesuai Bahan", layout="wide", page_icon="🥗")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .recipe-card { padding: 30px; border-radius: 20px; background-color: #ffffff; border: 2px solid #f0f2f6; box-shadow: 5px 5px 15px rgba(0,0,0,0.05); color: #2c3e50; }
    .stButton>button { border-radius: 12px; background: linear-gradient(45deg, #FF4B2B, #FF416C); color: white; border: none; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🥗 Chef AI: Kreasikan Bahan di Dapurmu")

# --- SIDEBAR: KONFIGURASI API ---
with st.sidebar:
    st.header("🔑 Akses AI")
    api_key_input = st.text_input("Gemini API Key:", type="password")
    st.info("Aplikasi ini akan meracik resep cerdas hanya dari bahan yang Anda sebutkan menggunakan Gemini 3 Flash.")

# --- FUNGSI AI ---
def generate_recipe(prompt, api_key):
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# --- INTERFACE UTAMA ---
st.subheader("📝 Masukkan Apa yang Anda Punya")

col1, col2 = st.columns([2, 1])

with col1:
    bahan_list = st.text_area(
        "Daftar Bahan & Bumbu:", 
        placeholder="Contoh: 2 butir telur, sebungkus mie instan, sawi, bawang putih, saus sambal...",
        height=150
    )
    
with col2:
    waktu = st.select_slider("Waktu Masak Maksimal:", options=["5 Menit", "15 Menit", "30 Menit", "1 Jam+"])
    porsi = st.number_input("Untuk Berapa Porsi?", min_value=1, max_value=10, value=1)

if st.button("🍳 Cari Resep yang Cocok"):
    if not api_key_input:
        st.error("Silakan isi API Key di sidebar terlebih dahulu!")
    elif not bahan_list:
        st.warning("Tuliskan dulu bahan yang Anda miliki di kolom di atas.")
    else:
        with st.spinner("Chef AI sedang meracik menu terbaik dari bahan Anda..."):
            prompt_masak = f"""
            Bertindaklah sebagai Chef Kreatif. 
            Saya HANYA memiliki bahan-bahan berikut: {bahan_list}.
            Batasan waktu: {waktu}.
            Jumlah porsi: {porsi}.
            
            Tugas Anda:
            1. Buatkan 1 nama masakan yang paling logis dan enak dari bahan tersebut.
            2. Sebutkan takaran bahan (gunakan bahan yang saya berikan).
            3. Berikan instruksi memasak yang ringkas dan jelas.
            4. Berikan alasan kenapa menu ini cocok (misal: praktis atau bergizi).
            
            Berikan jawaban dalam format Markdown yang rapi dan mudah dibaca.
            """
            res = generate_recipe(prompt_masak, api_key_input)
            st.markdown("### ✨ Hasil Kreasi Chef")
            st.markdown(f'<div class="recipe-card">{res}</div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("---")
st.caption("Masak Pintar dengan Gemini 3 Flash Preview | Pastikan ketersediaan bahan logis untuk dimasak.")
