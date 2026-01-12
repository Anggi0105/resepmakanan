import streamlit as st
import google.generativeai as genai

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Chef Gemini AI - Kreator Resep Pintar",
    page_icon="🍳",
    layout="centered"
)

# --- SISTEM KEAMANAN & INPUT API KEY ---
def init_gemini():
    # 1. Ambil dari Secrets jika tersedia (untuk deployment Cloud)
    api_key = st.secrets.get("GEMINI_API_KEY")
    
    # 2. Jika tidak ada di Secrets, munculkan kolom input di UI
    if not api_key:
        st.info("💡 Tips: Anda bisa mengatur API Key secara permanen di menu Secrets Streamlit Cloud.")
        api_key = st.text_input("Masukkan Google Gemini API Key Anda:", type="password")
    
    if api_key:
        try:
            # Konfigurasi eksplisit API Key
            genai.configure(api_key=api_key)
            
            # Memanggil model dengan cara paling standar untuk versi v1
            # Menghindari prefix 'models/' atau 'v1beta/' secara manual dalam string
            model = genai.GenerativeModel('gemini-1.5-flash')
            return model
        except Exception as e:
            st.error(f"Gagal konfigurasi AI: {e}")
            return None
    else:
        st.warning("🔑 Masukkan API Key untuk mengaktifkan Chef Gemini.")
        return None

# Inisialisasi Model
model = init_gemini()

# --- TAMPILAN ANTARMUKA ---
st.title("👨‍🍳 Chef Gemini: Racik Menu Sesukamu")
st.markdown("Sebutkan bumbu dan bahan yang ada di dapurmu. AI akan menciptakan resep unik yang lezat!")

with st.form("form_dapur"):
    col1, col2 = st.columns(2)
    with col1:
        bahan_utama = st.text_input("🥩 Bahan Utama", placeholder="Ayam, Telur, Tahu...")
    with col2:
        sayuran = st.text_input("🥦 Sayuran", placeholder="Bayam, Wortel, Kangkung...")
        
    bumbu = st.text_area("🧂 Bumbu & Bahan Lain", placeholder="Bawang putih, garam, saus tiram...")
    
    pedas = st.select_slider(
        "🔥 Tingkat Kepedasan",
        options=["Aman", "Sedang", "Pedas", "Lidah Terbakar"]
    )
    
    submit_button = st.form_submit_button(label="🪄 Racik Resep Sekarang")

# --- LOGIKA GENERASI RESEP ---
if submit_button:
    if not model:
        st.error("Silakan masukkan API Key yang valid terlebih dahulu.")
    elif not bahan_utama or not bumbu:
        st.warning("Mohon isi minimal 'Bahan Utama' dan 'Bumbu' agar Chef bisa bekerja!")
    else:
        with st.spinner('👨‍🍳 Sedang meramu resep rahasia...'):
            prompt = f"""
            Anda adalah seorang Chef Profesional. 
            Buatkan 1 resep kreatif berdasarkan input:
            - Bahan: {bahan_utama}, {sayuran}
            - Bumbu: {bumbu}
            - Pedas: {pedas}
            
            Berikan output Markdown: Nama Menu, Estimasi Waktu, Bahan, Langkah Memasak, dan Tips Chef.
            """
            
            try:
                # Menggunakan generate_content secara standar
                response = model.generate_content(prompt)
                st.markdown("---")
                st.success("✨ Resep Berhasil Diracik!")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")
                st.info("Solusi: Pastikan versi google-generativeai di requirements.txt sudah terbaru.")

st.markdown("---")
st.caption("Aplikasi ini menggunakan Google Gemini AI | Pastikan bahan layak konsumsi.")
