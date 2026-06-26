import streamlit as st
import os
from database.db import SessionLocal
from database.models import Meeting, ActionItem, init_db
from components.ui import setup_ui

# Set page config before anything else
st.set_page_config(page_title="Meeting Intelligence AI", page_icon="🎙️", layout="wide")

# Initialize database tables
init_db()

# Apply custom UI styling
setup_ui()

# Retrieve database statistics for dynamic dashboard presentation
db = SessionLocal()
total_meetings = 0
pending_tasks = 0
deal_stages = 0
if db:
    try:
        total_meetings = db.query(Meeting).count()
        pending_tasks = db.query(ActionItem).filter(ActionItem.status == 'Pending').count()
        deal_stages = db.query(Meeting.deal_stage).filter(Meeting.deal_stage.isnot(None)).distinct().count()
    except Exception as e:
        print(f"Error fetching stats for homepage: {e}")
    finally:
        db.close()

# Custom styles for the home page cards
st.markdown("""
<style>
/* Hero section styling */
.hero-container {
    background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
    border-radius: 16px;
    padding: 50px 40px;
    position: relative;
    overflow: hidden;
    border: 1px solid #334155;
    margin-bottom: 30px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
}
.hero-title {
    font-size: 3.2rem !important;
    font-weight: 700 !important;
    background: linear-gradient(90deg, #F1C40F 0%, #F39C12 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 15px;
    font-family: 'Outfit', sans-serif !important;
}
.hero-subtitle {
    font-size: 1.3rem !important;
    color: #94A3B8 !important;
    margin-bottom: 0px !important;
    font-weight: 400 !important;
    line-height: 1.6;
}

/* Service Card layout */
.service-card {
    background-color: #1E293B;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 30px 24px;
    height: 100%;
    min-height: 250px;
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s ease, border-color 0.3s ease;
    box-shadow: 0 4px 6px rgba(0,0,0,0.15);
    display: flex;
    flex-direction: column;
}
.service-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 12px 25px rgba(241, 196, 15, 0.15);
    border-color: #F1C40F;
}
.service-card-icon {
    font-size: 2.2rem;
    margin-bottom: 16px;
}
.service-card-title {
    color: #F1C40F !important;
    font-size: 1.35rem !important;
    font-weight: 600 !important;
    margin-bottom: 12px !important;
    font-family: 'Outfit', sans-serif !important;
}
.service-card-desc {
    color: #94A3B8;
    font-size: 0.95rem;
    line-height: 1.6;
    margin: 0;
}

/* CTA Sidebar Alert Banner */
.cta-banner {
    background-color: rgba(241, 196, 15, 0.08);
    border: 1px solid rgba(241, 196, 15, 0.3);
    border-left: 6px solid #F1C40F;
    border-radius: 8px;
    padding: 20px;
    margin-top: 30px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 15px;
}
.cta-text {
    color: #F8FAFC;
    font-size: 1.1rem;
    font-weight: 500;
    margin: 0;
}
</style>
""", unsafe_allow_html=True)

# 1. Hero Header
st.markdown("""
<div class="hero-container">
    <h1 class="hero-title">Meeting Intelligence AI 🎙️</h1>
    <p class="hero-subtitle">
        Transform raw sales meetings, audio notes, and video calls into actionable commercial summaries, 
        accurate transcripts, and professional reports instantly.
    </p>
</div>
""", unsafe_allow_html=True)

# 2. Dynamic Performance KPI metrics row
st.markdown("### 📊 System Status Overview")
m_col1, m_col2, m_col3 = st.columns(3)
m_col1.metric("Meetings Processed", total_meetings, help="Total number of meeting sessions recorded in the database")
m_col2.metric("Pending Action Items", pending_tasks, help="Tasks waiting completion across all meetings")
m_col3.metric("Distinct Deal Stages", deal_stages, help="Unique pipeline deal stages derived by Gemini analysis")

st.markdown("<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True)

# 3. Interactive features columns
st.markdown("### 🛠️ Capabilities")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="service-card">
        <div class="service-card-icon">📤</div>
        <div class="service-card-title">1. Multi-Format Input</div>
        <p class="service-card-desc">
            Directly upload video (MP4, MOV, MKV) and audio (MP3, WAV, M4A) files, or feed raw transcripts 
            from external notepad files and DOCX documents.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="service-card">
        <div class="service-card-icon">🧠</div>
        <div class="service-card-title">2. AI Transcription & Translation</div>
        <p class="service-card-desc">
            Powered by Whisper. Transcribes speech and auto-translates mixed linguistic audio (e.g., Tamil & English mix) 
            into structured English text scripts.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="service-card">
        <div class="service-card-icon">📋</div>
        <div class="service-card-title">3. Actionable Follow-Ups</div>
        <p class="service-card-desc">
            Instantly generates Minutes of Meeting (MoM), analyzes customer sentiment, evaluates deal stage closing probabilities, 
            drafts follow-up emails, and generates downloadable reports.
        </p>
    </div>
    """, unsafe_allow_html=True)

# 4. CTA Prompt banner
st.markdown("""
<div class="cta-banner">
    <div style="font-size: 1.5rem;">👈</div>
    <div class="cta-text">
        Ready to process your first meeting? Use the sidebar on the left and select <strong>dashboard</strong> to upload.
    </div>
</div>
""", unsafe_allow_html=True)
