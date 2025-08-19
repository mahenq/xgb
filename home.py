import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="👤 PREDIKSI KECEPATAN RATA-RATA BERSEPEDA BERDASARKAN KONDISI TOPOGRAFI DAN FAKTOR CUACA MENGGUNAKAN XGBOOST DARI DATA STRAVA",
    page_icon="👤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS (same as main app)
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
    
    .profile-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    
    .skill-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .contact-card {
        background: linear-gradient(135deg, #d299c2 0%, #fef9d7 100%);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        text-align: center;
    }
    
    .project-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    
    .timeline-item {
        background: white;
        padding: 1rem;
        border-left: 4px solid #3498db;
        margin: 0.5rem 0;
        border-radius: 5px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
            


            
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">TUGAS AKHIR</h1>', unsafe_allow_html=True)

    # Sidebar - Quick Info
    with st.sidebar:
        st.header("📋 Quick Info")
        
        st.markdown("""
        **👨‍💻 Developer**
        - **Name**: Rifqy Ramdhani Hakim
        - **Project**: Machine Learning
        - **Location**: Indonesia
        """)
        
        st.markdown("---")
        st.markdown("**🛠️ Tech Stack:**")
        st.markdown("""
        - Python, R, SQL
        - Scikit-learn, XGBoost
        - Streamlit, Flask
        - Plotly, Matplotlib, Seaborn
        - Pandas, NumPy, Jupyter
        """)

    # Profile Header
    st.markdown("""
    <div class="profile-card">
        <h2>PREDIKSI KECEPATAN RATA-RATA BERSEPEDA BERDASARKAN KONDISI TOPOGRAFI DAN FAKTOR CUACA MENGGUNAKAN XGBOOST DARI DATA STRAVA</h2>
    </div>
    """, unsafe_allow_html=True)

    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # About Me
        st.markdown('<div class="info-section">', unsafe_allow_html=True)
        st.subheader("🎯 Deskripsi Project")
        
        st.markdown("""
       Project ini disusun sebagai bagian dari pemenuhan syarat akademik pada jenjang Strata 1 (S1). 
        Penelitian sekaligus pengembangan yang dilakukan dalam project ini merupakan tugas 
                    akhir yang menjadi salah satu prasyarat kelulusan. Dengan demikian, project ini tidak hanya bertujuan untuk mengaplikasikan ilmu yang telah dipelajari selama masa studi, tetapi juga menjadi bentuk kontribusi penulis dalam bidang yang digeluti sesuai dengan program studi yang ditempuh.

        
        ### 🚴‍♂️ Background Bersepeda:
        Sebagai penggemar bersepeda aktif selama 5+ tahun, saya memahami betul tantangan dalam 
        merencanakan perjalanan bersepeda yang efektif. Pengalaman pribadi ini mendorong saya untuk 
        mengembangkan **Cycling Speed Predictor** - sebuah aplikasi yang menggabungkan passion saya 
        terhadap bersepeda dan expertise dalam machine learning.
        
        ### 💡 Motivasi Proyek:
        - Membantu komunitas bersepeda Indonesia
        - Meningkatkan keselamatan pengendara
        - Memberikan insight berbasis data untuk perencanaan rute
        - Mengoptimalkan performa dan pengalaman bersepeda
        """)
        st.markdown('</div>', unsafe_allow_html=True)


    # Development Process
    st.subheader("⚙️ Development Process")
    
    process_tabs = st.tabs(["📊 Data Collection", "🔧 Model Development", "🚀 Deployment", "📈 Results"])
    
    with process_tabs[0]:
        st.markdown("""
        ### 📊 Data Collection & Preprocessing
        
        **Data Sources:**
        - Strava API untuk data perjalanan bersepeda
        - Weather API untuk data cuaca historis
        - Topografi data dari elevation APIs
        
        **Preprocessing Steps:**
        - Data cleaning dan outlier removal
        - Feature engineering (17 features)
        - Data augmentation untuk balance dataset
        - Train-test split dengan temporal consideration
        """)
    
    with process_tabs[1]:
        st.markdown("""
        ### 🔧 Model Development
        
        **Algorithm Selection:**
        - XGBoost memberikan performa terbaik
        - Hyperparameter tuning dengan GridSearchCV
        
        **Feature Engineering:**
        - Categorical encoding untuk time, weather, terrain
        - Interaction features (speed/elevation ratio)
        - Temporal features (hour, day of week)
        """)
    
    with process_tabs[2]:
        st.markdown("""
        ### 🚀 Deployment
        
        **Tech Stack:**
        - Streamlit untuk web application
        - Plotly untuk interactive visualizations
        - Joblib untuk model serialization
        - GitHub untuk version control
        
        **Features Implemented:**
        - Interactive visualizations
        - Comprehensive analysis
        - Smart recommendations
        """)
    
    with process_tabs[3]:
        st.markdown("""
        ### 📈 Results & Impact
        
        **Model Performance:**
        - **R² Score**: 0.892 (excellent accuracy)
        - **MAE**: 1.23 km/h (practical precision)
        - **RMSE**: 1.58 km/h
        
        **User Impact:**
        - Better trip planning for cyclists
        - Improved safety through realistic expectations
        - Data-driven insights for performance optimization
        """)

    # Future Plans
    st.markdown('<div class="info-section">', unsafe_allow_html=True)
    st.subheader("🚀 Future Plans & Improvements")
    
    future_col1, future_col2 = st.columns(2)
    
    with future_col1:
        st.markdown("""
        **📱 App Enhancements:**
        - Mobile-responsive design
        - User authentication & history
        - Route planning integration
        - Real-time weather integration
        
        **🤖 Model Improvements:**
        - Deep learning models (LSTM for time series)
        - Real-time model updating
        - Personalization based on user history
        """)
    
    with future_col2:
        st.markdown("""
        **🌍 Community Features:**
        - Social sharing capabilities
        - Community challenges
        - Performance comparisons
        - Route recommendations
        
        **📊 Analytics Dashboard:**
        - Performance trends analysis
        - Seasonal pattern insights
        - Training recommendations
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)


    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #7f8c8d; margin: 2rem 0;">
        <p>👤 <strong>Rifqy Ramdhani Hakim</strong> | Tugas Akhir</p>
    </div>
    """, unsafe_allow_html=True)


    

if __name__ == "__main__":
    main()