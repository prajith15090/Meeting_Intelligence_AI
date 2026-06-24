import streamlit as st
import os

# Set page config before anything else
st.set_page_config(page_title="Sales Meeting Intelligence", page_icon="📈", layout="wide")

# Initialize database
from database.models import init_db
init_db()

from components.ui import setup_ui
setup_ui()
# Main page content
st.title("Sales Meeting Intelligence 🎙️")
st.markdown("""
Welcome to the **Sales Meeting Intelligence** app.
This tool helps you transcribe, summarize, and extract actionable insights from your sales meetings.
""")

st.info("👈 Please select a page from the sidebar to get started.")

st.markdown("### Features")
st.markdown("""
- **Dashboard**: Upload an audio file and analyze your meeting.
- **History**: View past meetings and generate PDF reports.
""")
