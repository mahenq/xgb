import streamlit as st
from PIL import Image
import os

# Page config
st.set_page_config(
    page_title="👤 Profil & Tugas Akhir", 
    page_icon="👤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS untuk styling modern
st.markdown("""
    <style>
      .main-header {
    font-size: 3rem;
    font-weight: bold;
    text-align: center;
    color: black; /* warna font hitam */
    margin-bottom: 2rem;
    text-shadow: none; /* hilangkan shadow */
}

    
    .profile-main-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 20px;
        color: white;
        margin: 2rem 0;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        position: relative;
        overflow: hidden;
    }
    
    .profile-main-card::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 100%;
        height: 100%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        border-radius: 50%;
    }
    
    .profile-image-container {
        display: flex;
        justify-content: center;
        margin-bottom: 1.5rem;
        position: relative;
        z-index: 2;
    }
    
    .profile-image-container img,
    .stImage > div > img {
        border-radius: 50% !important;
        width: 180px !important;
        height: 180px !important;
        object-fit: cover !important;
        border: 6px solid rgba(255,255,255,0.2) !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3) !important;
        transition: transform 0.3s ease !important;
        display: block !important;
        margin: 0 auto !important;
    }
    
    .profile-image-container img:hover,
    .stImage > div > img:hover {
        transform: scale(1.05) !important;
    }
    
    .profile-info {
        text-align: center;
        position: relative;
        z-index: 2;
    }
    
    .profile-info h2 {
        margin: 0 0 0.5rem 0;
        font-size: 2.5rem;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .profile-info .student-id {
        font-size: 1.3rem;
        font-weight: 500;
        opacity: 0.9;
        margin-bottom: 0.5rem;
    }
    
    .profile-info .program {
        font-size: 1.1rem;
        opacity: 0.8;
        margin-bottom: 0.3rem;
    }
    
    .profile-info .university {
        font-size: 1.1rem;
        opacity: 0.8;
    }
    
    .thesis-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 2rem 0;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        position: relative;
        overflow: hidden;
    }
    
    .thesis-card::before {
        content: '📋';
        position: absolute;
        top: -10px;
        right: -10px;
        font-size: 4rem;
        opacity: 0.1;
    }
    
    .thesis-title {
        font-size: 1.8rem;
        font-weight: bold;
        margin-bottom: 1rem;
        line-height: 1.3;
    }
    
    .thesis-description {
        font-size: 1rem;
        line-height: 1.6;
        opacity: 0.95;
    }
    
    .contact-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 2rem;
        color: white;
        margin-top: 2rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    
    .contact-section h3 {
        text-align: center;
        font-size: 1.8rem;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    
    .contact-card {
        background: rgba(255,255,255,0.15);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        text-align: center;
        font-size: 1rem;
        font-weight: 500;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 0.5rem;
        transition: transform 0.3s ease, background 0.3s ease;
        cursor: pointer;
    }
    
    .contact-card:hover {
        transform: translateY(-5px);
        background: rgba(255,255,255,0.25);
    }
    
    .contact-card h4 {
        margin-bottom: 0.5rem;
        font-size: 1.2rem;
        font-weight: 600;
    }
    
    .contact-card p {
        margin: 0;
        opacity: 0.9;
    }
    
    .sidebar-info {
        background: linear-gradient(135deg, #d299c2 0%, #fef9d7 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .quick-stats {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        text-align: center;
    }
    
    .stat-item {
        margin: 0.5rem 0;
        font-weight: 500;
    }
    
    .footer {
        text-align: center;
        color: #7f8c8d;
        margin: 3rem 0 2rem 0;
        padding: 2rem;
        border-top: 2px solid #ecf0f1;
    }
    </style>
""", unsafe_allow_html=True)

def load_profile_image():
    """
    Function to load profile image with multiple path attempts
    Returns base64 encoded image for direct HTML embedding
    """
    import base64
    from io import BytesIO
    
    # Get the current working directory
    current_dir = os.getcwd()
    
    # Define possible paths for the profile image
    possible_paths = [
        "assets/profile.jpg",
        "./assets/profile.jpg",
        os.path.join(current_dir, "assets", "profile.jpg"),
        os.path.join(os.path.dirname(__file__), "assets", "profile.jpg") if '__file__' in globals() else None,
        "profile.jpg",
        "./profile.jpg"
    ]
    
    # Remove None values
    possible_paths = [path for path in possible_paths if path is not None]
    
    # Try to load image from each path
    for path in possible_paths:
        try:
            if os.path.exists(path):
                with open(path, "rb") as img_file:
                    img_bytes = img_file.read()
                    img_base64 = base64.b64encode(img_bytes).decode()
                    return img_base64, path
        except Exception as e:
            continue
    
    return None, None

def main():
    # Header
    st.markdown('<h1 class="main-header">👤 Profil & Tugas Akhir</h1>', unsafe_allow_html=True)

    # Profile Card dengan gambar
    st.markdown('<div class="profile-main-card">', unsafe_allow_html=True)
    
    # Load and display profile image
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        # Try to load the profile image
        img_base64, image_path = load_profile_image()
        
        if img_base64 is not None:
            # Display image using HTML div with circular frame
            st.markdown(f"""
            <div style="display: flex; justify-content: center; margin-bottom: 1.5rem;">
                <div style="
                    width: 180px; 
                    height: 180px; 
                    border-radius: 50%; 
                    background-image: url(data:image/jpeg;base64,{img_base64});
                    background-size: cover;
                    background-position: center;
                    background-repeat: no-repeat;
                    border: 6px solid rgba(255,255,255,0.2);
                    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                    transition: transform 0.3s ease;
                ">
                </div>
            </div>
            <style>
            div[style*="background-image"]:hover {{
                transform: scale(1.05);
            }}
            </style>
            """, unsafe_allow_html=True)
        else:
            # Fallback to placeholder if image not found
            st.markdown("""
            <div style="display: flex; justify-content: center; margin-bottom: 1.5rem;">
                <div style="
                    width: 180px; 
                    height: 180px; 
                    border-radius: 50%; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    display: flex; 
                    align-items: center; 
                    justify-content: center;
                    font-size: 4rem;
                    border: 6px solid rgba(255,255,255,0.2);
                    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                    transition: transform 0.3s ease;
                ">
                    👤
                </div>
            </div>
            <style>
            div[style*="linear-gradient"]:hover {
                transform: scale(1.05);
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Show debug information about attempted paths
            with st.expander("🔍 Debug Info - Lokasi file yang dicari"):
                current_dir = os.getcwd()
                st.write(f"**Current working directory:** `{current_dir}`")
                st.write("**Paths yang dicoba:**")
                possible_paths = [
                    "assets/profile.jpg",
                    "./assets/profile.jpg",
                    os.path.join(current_dir, "assets", "profile.jpg"),
                    "profile.jpg",
                    "./profile.jpg"
                ]
                
                for path in possible_paths:
                    exists = "✅" if os.path.exists(path) else "❌"
                    st.write(f"- {exists} `{path}`")
                
                st.write("**Files in current directory:**")
                try:
                    files = os.listdir(current_dir)
                    for file in sorted(files):
                        if os.path.isdir(file):
                            st.write(f"📁 {file}/")
                        else:
                            st.write(f"📄 {file}")
                except:
                    st.write("Cannot list directory contents")
    
    st.markdown("""
        <div class="profile-info">
            <h2>Rifqy Ramdhani Hakim</h2>
            <p class="student-id">3260210111</p>
            <p class="program">Program Studi Teknik Informatika</p>
            <p class="university">Universitas Islam Sultan Agung, Semarang</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Tugas Akhir Section
    st.markdown("""
    <div class="thesis-card">
        <div class="thesis-title">
            🚴‍♂️ PREDIKSI KECEPATAN RATA-RATA BERSEPEDA BERDASARKAN KONDISI TOPOGRAFI DAN FAKTOR CUACA MENGGUNAKAN XGBOOST DARI DATA STRAVA
        </div>
        <div class="thesis-description">
            Proyek penelitian yang mengembangkan model machine learning untuk memprediksi kecepatan rata-rata bersepeda 
            berdasarkan berbagai faktor seperti topografi, kondisi cuaca, dan data historis dari platform Strava. 
            Menggunakan algoritma XGBoost dengan akurasi tinggi untuk memberikan prediksi yang akurat dan berguna 
            bagi komunitas bersepeda dalam merencanakan perjalanan mereka.
            <br><br>
            <strong>🎯 Fitur Utama:</strong>
            <ul style="margin-top: 1rem; text-align: left;">
                <li>Prediksi kecepatan berbasis ML dengan akurasi 89.2%</li>
                <li>Analisis 17+ faktor yang mempengaruhi performa bersepeda</li>
                <li>Interface web interaktif menggunakan Streamlit</li>
                <li>Visualisasi data komprehensif dengan Plotly</li>
                <li>Integrasi data real-time dari berbagai API</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Project Timeline
    st.subheader("📅 Timeline Pengerjaan")
    
    timeline_tabs = st.tabs(["🔍 Research", "💻 Development", "🧪 Testing", "🚀 Deployment"])
    
    with timeline_tabs[0]:
        st.markdown("""
        **🔍 Phase 1: Research & Data Collection (2 bulan)**
        - Studi literatur tentang faktor-faktor yang mempengaruhi kecepatan bersepeda
        - Pengumpulan data dari Strava API dan weather APIs
        - Analisis eksplorasi data dan identifikasi pola
        - Pemilihan features yang relevan
        """)
    
    with timeline_tabs[1]:
        st.markdown("""
        **💻 Phase 2: Model Development (2 bulan)**
        - Feature engineering dan preprocessing data
        - Implementasi dan tuning model XGBoost
        - Perbandingan dengan algoritma ML lainnya
        - Optimasi hyperparameter untuk performa terbaik
        """)
    
    with timeline_tabs[2]:
        st.markdown("""
        **🧪 Phase 3: Testing & Validation (1 bulan)**
        - Cross-validation dan testing dengan data baru
        - Evaluasi model dengan berbagai metrik
        - Testing aplikasi web dan user interface
        - Bug fixing dan optimization
        """)
    
    with timeline_tabs[3]:
        st.markdown("""
        **🚀 Phase 4: Deployment & Documentation (1 bulan)**
        - Deploy aplikasi web dengan Streamlit
        - Dokumentasi teknis dan user guide
        - Presentasi dan demo aplikasi
        - Finalisasi laporan tugas akhir
        """)

    # Informasi Kontak dengan styling modern
    st.markdown("""
    <div class="contact-section">
        <h3>📞 Informasi Kontak</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
            <div class="contact-card">
                <h4>📧 Email</h4>
                <p>rifqy.ramdhani@email.com</p>
            </div>
            <div class="contact-card">
                <h4>📱 Telepon</h4>
                <p>081548928174</p>
            </div>
            <div class="contact-card">
                <h4>🌐 LinkedIn</h4>
                <p>linkedin.com/in/rifqyramdhani</p>
            </div>
            <div class="contact-card">
                <h4>🔗 GitHub</h4>
                <p>https://github.com/Rifqyyyy</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div class="footer">
        <p><strong>👤 Profil & Tugas Akhir</strong> | Rifqy Ramdhani Hakim</p>
        <p><em>"PREDIKSI KECEPATAN RATA-RATA BERSEPEDA BERDASARKAN KONDISI TOPOGRAFI DAN FAKTOR CUACA MENGGUNAKAN XGBOOST DARI DATA STRAVA"</em></p>
        <p>© 2024 Rifqy Ramdhani Hakim - Teknik Informatika UNISSULA</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()