import streamlit as st
from google import genai

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Chef AI: Masak Pintar (Gemini 3)", layout="wide", page_icon="🍳")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .recipe-box { padding: 25px; border: 1px solid #e0e0e0; border-radius: 15px; background-color: #f9f9f9; color: #333; line-height: 1.6; }
    .stButton>button { width: 100%; border-radius: 10px; height: 50px; font-weight: bold; background-color: #ff4b4b; color: white; }
    .stButton>button:hover { background-color: #ff3333; border: 1px solid #ff3333; }
    </style>
    """, unsafe_allow_html=True)

st.title("👨‍🍳 Chef AI: Inspirasi Resep Gemini 3")

# --- SIDEBAR: KONFIGURASI API ---
with st.sidebar:
    st.header("🔑 Konfigurasi")
    api_key_input = st.text_input("Masukkan Gemini API Key:", type="password")
    st.info("Aplikasi ini menggunakan Model Gemini 3 Flash Preview untuk meracik resep masakan secara cerdas.")
    st.markdown("[Dapatkan API Key Gratis di Sini](https://aistudio.google.com/)")

# --- FUNGSI AI (SDK GOOGLE GENAI TERBARU) ---
def generate_recipe(prompt, api_key):
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"Error: Pastikan API Key benar. Detail: {str(e)}"

# --- TABS INTERFACE ---
tab1, tab2 = st.tabs(["🥘 Racik dari Bahan Sisa", "🔎 Cari Inspirasi Menu"])

with tab1:
    st.subheader("Punya Bahan Apa di Dapur?")
    col_bahan, col_bumbu = st.columns(2)
    
    with col_bahan:
        protein = st.text_input("Bahan Utama (Protein/Sayur):", placeholder="Contoh: Ayam, Tahu, Telur, Kangkung")
    with col_bumbu:
        bumbu = st.text_input("Bumbu yang Tersedia:", placeholder="Contoh: Bawang putih, Saus tiram, Kecap, Cabai")
    
    level_pedas = st.select_slider("Tingkat Kepedasan:", options=["Tidak Pedas", "Sedang", "Pedas", "Lidah Terbakar"])

    if st.button("🪄 Sulap Jadi Resep!"):
        if not api_key_input:
            st.error("Silakan isi API Key di sidebar terlebih dahulu!")
        elif not protein or not bumbu:
            st.warning("Mohon isi bahan dan bumbu yang Anda miliki.")
        else:
            with st.spinner("Chef AI sedang memikirkan menu terbaik..."):
                prompt_racik = f"""
                Bertindaklah sebagai Chef Profesional. 
                Saya memiliki bahan utama: {protein} 
                Dan bumbu: {bumbu}.
                Tingkat kepedasan yang diinginkan: {level_pedas}.
                
                Tugas Anda:
                1. Berikan Nama Menu yang unik dan menggugah selera.
                2. Berikan daftar bahan lengkap (asumsikan bumbu dasar seperti garam/minyak tersedia).
                3. Berikan instruksi memasak langkah-demi-langkah yang jelas.
                4. Berikan 'Tips Rahasia Chef' agar masakan lebih enak.
                
                Gunakan format Markdown yang rapi.
                """
                res = generate_recipe(prompt_racik, api_key_input)
                st.markdown("### ✨ Rekomendasi Masakan")
                st.markdown(f'<div class="recipe-box">{res}</div>', unsafe_allow_html=True)

with tab2:
    st.subheader("Cari Detail Resep Spesifik")
    nama_masakan = st.text_input("Nama masakan yang ingin diketahui resepnya:", placeholder="Contoh: Rendang Daging, Fettuccine Carbonara, Seblak")
    
    if st.button("Dapatkan Resep Lengkap"):
        if not api_key_input:
            st.error("Isi API Key dulu!")
        elif not nama_masakan:
            st.warning("Masukkan nama masakan.")
        else:
            with st.spinner(f"Mencari resep autentik {nama_masakan}..."):
                prompt_cari = f"Berikan resep lengkap, sejarah singkat, estimasi kalori, dan cara memasak untuk menu: {nama_masakan}"
                res = generate_recipe(prompt_cari, api_key_input)
                st.markdown(f'<div class="recipe-box">{res}</div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("---")
st.caption("Chef AI Intelligence | Powered by Gemini 3 Flash SDK 1.0")
