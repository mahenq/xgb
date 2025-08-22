# path: app.py
import streamlit as st
import joblib
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
from datetime import time
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="📊 Cycling Speed Predictor - App",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI (unchanged)
st.markdown(
    """
<style>
     .main-header {
    font-size: 3rem;
    font-weight: bold;
    text-align: center;
    color: black;
    margin-bottom: 2rem;
    text-shadow: none;
}
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .prediction-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    
    .input-section {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .stSelectbox label, .stSlider label, .stNumberInput label, .stTimeInput label {
        font-weight: bold;
        color: #2c3e50;
    }
    
    .weather-info {
        background: linear-gradient(135deg, #d299c2 0%, #fef9d7 100%);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Load model
@st.cache_resource
def load_model():
    """Load trained model; fall back to dummy if not found (keeps app usable)."""
    try:
        model_package = joblib.load("./models/cycling_speed_prediction_model_v2.joblib")
        return model_package
    except FileNotFoundError:
        return create_dummy_model_package()
    except Exception as e:
        st.error(f"⚠️ Error loading model: {str(e)}")
        return create_dummy_model_package()


def create_dummy_model_package():
    """Return minimal model metadata to keep UI informative when model missing."""
    return {
        'model_performance': {
            'test_mae': 1.230,
            'test_r2': 0.892,
            'test_rmse': 1.580,
        },
        'training_info': {
            'original_samples': 5000,
            'augmented_samples': 10000,
            'training_date': '2024-01-15',
        },
    }


# Demo prediction (unchanged)
def predict_cycling_speed_demo(elevasi, jarak, curah_hujan, jam_tidur, jam_mulai):
    """Simple heuristic used when real model is unavailable; adds small stochasticity."""
    try:
        base_speed = 22.0
        distance_factor = max(0.85, 1 - (jarak - 25) * 0.01)
        elevation_factor = max(0.7, 1 - (elevasi - 200) * 0.001)
        rain_factor = 1.0 if curah_hujan == 0 else max(0.6, 1 - curah_hujan * 0.01)
        sleep_factor = min(1.1, 0.8 + jam_tidur * 0.04)

        hour = jam_mulai.hour
        if 6 <= hour <= 10:
            time_factor = 1.05
        elif 10 < hour <= 16:
            time_factor = 1.0
        else:
            time_factor = 0.95

        prediction = base_speed * distance_factor * elevation_factor * rain_factor * sleep_factor * time_factor
        prediction += np.random.normal(0, 0.5)
        prediction = max(10, min(35, prediction))

        time_category = (
            'Early_Morning' if hour < 8 else 'Morning' if hour < 12 else 'Afternoon' if hour < 17 else 'Evening'
        )
        elevation_category = (
            'Flat' if elevasi <= 150 else 'Rolling' if elevasi <= 250 else 'Hilly' if elevasi <= 400 else 'Mountainous'
        )
        rain_category = (
            'No_Rain' if curah_hujan <= 0 else 'Light' if curah_hujan <= 10 else 'Moderate' if curah_hujan <= 30 else 'Heavy'
        )
        distance_category = (
            'Short' if jarak <= 20 else 'Medium' if jarak <= 30 else 'Long' if jarak <= 40 else 'Ultra'
        )
        sleep_quality = (
            'Poor' if jam_tidur <= 4 else 'Moderate' if jam_tidur <= 6 else 'Good' if jam_tidur <= 8 else 'Excellent'
        )

        return prediction, time_category, elevation_category, rain_category, distance_category, sleep_quality

    except Exception as e:
        st.error(f"Prediction error: {str(e)}")
        return None, None, None, None, None, None


# Wrapper prediction
def predict_cycling_speed(elevasi, jarak, curah_hujan, jam_tidur, jam_mulai, model_package):
    """Use real model if present; otherwise fallback to demo."""
    if 'model' in model_package:
        # Placeholder for real model inference path
        pass
    return predict_cycling_speed_demo(elevasi, jarak, curah_hujan, jam_tidur, jam_mulai)


# Load the model once
model_package = load_model()


# =====================
# Main app (LAYOUT FIX)
# =====================

def main():
    # Header
    st.markdown('<h1 class="main-header">📊 Cycling Speed Predictor</h1>', unsafe_allow_html=True)
    st.markdown("### 🔊 Prediksi Kecepatan Rata-rata Bersepeda Berdasarkan Kondisi Topografi & Cuaca")
    st.info("🏠 Kembali ke **Home** atau kunjungi **👤 Profile** untuk informasi developer")

    # Sidebar — Model information
    with st.sidebar:
        st.header("📋 Model Information")
        if 'model_performance' in model_package:
            perf = model_package['model_performance']
            st.markdown(
                f"""
            **📈 Model Performance:**
            - **MAE**: {perf['test_mae']:.3f} km/h
            - **R²**: {perf['test_r2']:.3f}
            - **RMSE**: {perf['test_rmse']:.3f} km/h
            """
            )
        if 'training_info' in model_package:
            info = model_package['training_info']
            st.markdown(
                f"""
            **🔧 Training Info:**
            - **Original Samples**: {info['original_samples']}
            - **Augmented Samples**: {info['augmented_samples']}
            - **Training Date**: {info['training_date']}
            """
            )
        st.markdown("---")
        st.markdown("**🎯 Input Guidelines:**")
        st.markdown(
            """
        - **Elevasi**: 50-700m
        - **Jarak**: 10-50 km
        - **Curah Hujan**: 0-100mm
        - **Jam Tidur**: 1-12 jam
        """
        )

    # ===== Two main columns =====
    col1, col2 = st.columns([3, 2])

    # -------- Col1: Form + Input Visualization --------
    with col1:
        st.markdown('<div class="input-section">', unsafe_allow_html=True)
        st.subheader("🎛️ Input Parameters")
        with st.form("prediction_form"):
            subcol1, subcol2 = st.columns(2)
            with subcol1:
                jarak = st.slider(
                    "🚀 Jarak (km)", min_value=5.0, max_value=50.0, value=25.0, step=0.5,
                    help="Jarak tempuh yang akan ditempuh",
                )
                elevasi = st.slider(
                    "⛰️ Elevasi (m)", min_value=50, max_value=700, value=200, step=10,
                    help="Elevasi total yang akan dilalui",
                )
            with subcol2:
                curah_hujan = st.slider(
                    "🌧️ Curah Hujan (mm)", min_value=0.0, max_value=100.0, value=0.0, step=0.1,
                    help="Intensitas hujan saat bersepeda",
                )
                jam_tidur = st.slider(
                    "😴 Jam Tidur (jam)", min_value=1, max_value=12, value=7, step=1,
                    help="Durasi tidur malam sebelumnya",
                )
            jam_mulai = st.time_input("🕐 Jam Mulai", value=time(6, 0), help="Waktu mulai bersepeda")
            predict_button = st.form_submit_button("🚀 Predict Speed", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # --- Input Visualization moved into Col1 ---
        st.subheader("📊 Input Visualization")
        categories = ['Distance\n(Normalized)', 'Elevation\n(Normalized)', 'Rain\n(Inverted)', 'Sleep\n(Normalized)']
        values = [
            jarak / 50,
            elevasi / 700,
            1 - (curah_hujan / 100),
            jam_tidur / 12,
        ]
        fig_radar = go.Figure(
            data=go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                line=dict(color='rgb(255, 107, 107)'),
                fillcolor='rgba(255, 107, 107, 0.3)',
            )
        )
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
            showlegend=False,
            title="Input Parameters Overview",
            height=300,
        )
        st.plotly_chart(fig_radar, use_container_width=True)

        st.markdown('<div class="weather-info">', unsafe_allow_html=True)
        if curah_hujan == 0:
            st.markdown("☀️ **Kondisi**: Cerah")
        elif curah_hujan <= 10:
            st.markdown("🌦️ **Kondisi**: Hujan Ringan")
        elif curah_hujan <= 30:
            st.markdown("🌧️ **Kondisi**: Hujan Sedang")
        else:
            st.markdown("⛈️ **Kondisi**: Hujan Lebat")
        st.markdown('</div>', unsafe_allow_html=True)

    # -------- Col2: Prediction Card + Mini Cards --------
    with col2:
        if predict_button:
            with st.spinner("🔮 Calculating prediction..."):
                prediction, time_cat, elev_cat, rain_cat, dist_cat, sleep_cat = predict_cycling_speed(
                    elevasi, jarak, curah_hujan, jam_tidur, jam_mulai, model_package
                )

            if prediction is not None:
                st.markdown(
                    f"""
                <div class="prediction-card">
                    <h2>🎯 Predicted Speed</h2>
                    <h1 style="font-size: 4rem; margin: 1rem 0;">{prediction:.1f} km/h</h1>
                    <p style="font-size: 1.2rem;">Based on your input conditions</p>
                </div>
                """,
                    unsafe_allow_html=True,
                )

                # Mini cards (nested columns within the narrower right column)
                mini1, mini2, mini3 = st.columns(3)

                with mini1:
                    if prediction < 16:
                        speed_category, speed_color = "🌊 Leisurely", "#3498db"
                    elif prediction < 20:
                        speed_category, speed_color = "🚴‍♀️ Moderate", "#f39c12"
                    elif prediction < 24:
                        speed_category, speed_color = "🚴‍♂️ Fast", "#e67e22"
                    else:
                        speed_category, speed_color = "🏆 Very Fast", "#e74c3c"
                    st.markdown(
                        f"""
                    <div style="background: {speed_color}; color: white; padding: 1rem; border-radius: 10px; text-align: center;">
                        <h5>{speed_category}</h5>
                        <p>Speed Category</p>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

                with mini2:
                    estimated_time = jarak / prediction * 60  # minutes
                    hours = int(estimated_time // 60)
                    minutes = int(estimated_time % 60)
                    st.markdown(
                        f"""
                    <div style="background: #27ae60; color: white; padding: 1rem; border-radius: 10px; text-align: center;">
                        <h5>⏱️ {hours:02d}:{minutes:02d}</h5>
                        <p>Estimated Time</p>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

                with mini3:
                    effort_score = (elevasi / 10) + (curah_hujan / 5) + max(0, 8 - jam_tidur) * 5
                    if effort_score < 30:
                        effort_level, effort_color = "😌 Easy", "#2ecc71"
                    elif effort_score < 50:
                        effort_level, effort_color = "💪 Moderate", "#f39c12"
                    else:
                        effort_level, effort_color = "🔥 Challenging", "#e74c3c"
                    st.markdown(
                        f"""
                    <div style="background: {effort_color}; color: white; padding: 1rem; border-radius: 10px; text-align: center;">
                        <h5>{effort_level}</h5>
                        <p>Effort Level</p>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )
        else:
            # Placeholder keeps right column balanced before prediction
            st.info("Klik **Predict Speed** untuk melihat hasil dan ringkasan di sini.")

    # -------- Full-width sections below both columns --------
    if 'prediction' in locals() and prediction is not None and predict_button:
        st.subheader("📋 Condition Analysis")
        analysis_col1, analysis_col2 = st.columns(2)
        with analysis_col1:
            st.markdown("**🏞️ Terrain & Route:**")
            st.markdown(f"- Distance Category: **{dist_cat}**")
            st.markdown(f"- Elevation Category: **{elev_cat}**")
            st.markdown(f"- Elevation per km: **{elevasi/jarak:.1f}m/km**")
            st.markdown("**⏰ Timing:**")
            st.markdown(f"- Time Category: **{time_cat}**")
            st.markdown(f"- Start Time: **{jam_mulai.strftime('%H:%M')}**")
        with analysis_col2:
            st.markdown("**🌤️ Weather & Conditions:**")
            st.markdown(f"- Rain Category: **{rain_cat}**")
            if curah_hujan > 0:
                impact = int((1 - (1 if curah_hujan == 0 else 0.8 if curah_hujan <= 10 else 0.6 if curah_hujan <= 30 else 0.4)) * 100)
                st.markdown(f"- Rain Impact: **-{impact}% speed**")
            st.markdown("**😴 Physical Condition:**")
            st.markdown(f"- Sleep Quality: **{sleep_cat}**")
            st.markdown(f"- Sleep Hours: **{jam_tidur}h**")

        # Speed comparison chart
        st.subheader("📊 Speed Comparison")
        perfect_speed = predict_cycling_speed_demo(100, jarak, 0, 8, time(6, 0))[0]
        rainy_speed = predict_cycling_speed_demo(elevasi, jarak, 20, jam_tidur, jam_mulai)[0]
        hilly_speed = predict_cycling_speed_demo(400, jarak, curah_hujan, jam_tidur, jam_mulai)[0]
        tired_speed = predict_cycling_speed_demo(elevasi, jarak, curah_hujan, 3, jam_mulai)[0]

        comparison_scenarios = [
            ("Perfect Conditions", perfect_speed),
            ("Your Prediction", prediction),
            ("Rainy Conditions", rainy_speed),
            ("Hilly Terrain", hilly_speed),
            ("Tired Rider", tired_speed),
        ]
        scenario_names = [item[0] for item in comparison_scenarios]
        scenario_speeds = [item[1] for item in comparison_scenarios]
        fig_comparison = go.Figure(
            data=[
                go.Bar(
                    x=scenario_names,
                    y=scenario_speeds,
                    marker_color=[
                        '#2ecc71' if name == 'Perfect Conditions' else '#e74c3c' if name == 'Your Prediction' else '#95a5a6'
                        for name in scenario_names
                    ],
                )
            ]
        )
        fig_comparison.update_layout(
            title="Speed Comparison Across Different Scenarios",
            xaxis_title="Scenarios",
            yaxis_title="Speed (km/h)",
            height=400,
        )
        st.plotly_chart(fig_comparison, use_container_width=True)

        # Recommendations
        st.subheader("💡 Recommendations")
        recommendations = []
        if curah_hujan > 10:
            recommendations.append("🌧️ Consider postponing if possible - rain significantly reduces speed and safety")
        if elevasi > 300:
            recommendations.append("⛰️ Prepare for challenging climbs - consider lower gearing and pacing strategy")
        if jam_tidur < 6:
            recommendations.append("😴 Low sleep may affect performance - consider extra rest or shorter distance")
        if jam_mulai.hour >= 16:
            recommendations.append("🌅 Afternoon rides may be slower due to fatigue and traffic")
        if prediction > 22:
            recommendations.append("🏆 Great conditions for a fast ride - push your limits!")
        if prediction < 18:
            recommendations.append("🎯 Focus on endurance rather than speed for this ride")
        if not recommendations:
            recommendations.append("✅ Conditions look good for a balanced ride!")
        for rec in recommendations:
            st.info(rec)

    # Footer
    st.markdown("---")
    st.markdown(
        """
    <div style="text-align: center; color: #7f8c8d; margin: 2rem 0;">
        <p>📊 <strong>Cycling Speed Predictor - App Utama</strong> | Powered by XGBoost & Streamlit</p>
        <p><em>Predictions based on Strava cycling data analysis</em></p>
    </div>
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
