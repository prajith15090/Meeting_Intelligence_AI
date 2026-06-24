import streamlit as st
import base64
import os

def setup_ui():
    """
    Applies custom styling to the Streamlit app matching "The Yellow Network" branding
    with a premium Dark Navy theme and handles placing the logo.
    """
    
    # Base64 encode logo for sidebar and CSS
    logo_path = "logo.png"
    logo_base64 = ""
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as image_file:
            logo_base64 = base64.b64encode(image_file.read()).decode()
            
        # Display logo in top right corner as a polished badge
        st.markdown(
            f'''
            <style>
            .top-right-logo {{
                position: fixed;
                top: 15px;
                right: 20px;
                width: 120px;
                z-index: 999999;
                background-color: #FFFFFF;
                padding: 6px 12px;
                border-radius: 8px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
                border: 1px solid rgba(255, 255, 255, 0.1);
                transition: transform 0.3s ease;
            }}
            .top-right-logo:hover {{
                transform: scale(1.05);
            }}
            </style>
            <img src="data:image/png;base64,{logo_base64}" class="top-right-logo">
            ''',
            unsafe_allow_html=True,
        )
    else:
        st.sidebar.markdown("### The Yellow Network")

    # Inject Custom CSS
    st.markdown(f"""
    <style>
    /* Import Premium Modern Typography */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"], .stApp {{
        font-family: 'Outfit', sans-serif !important;
    }}

    /* Global Dark Theme Corrections */
    .stApp {{
        background-color: #0F172A;
        color: #F8FAFC;
    }}
    
    /* Primary & Download Buttons */
    .stButton > button, .stDownloadButton > button {{
        background-color: #F1C40F !important;
        color: #0F172A !important;
        border-radius: 8px !important;
        border: none !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        font-weight: 600 !important;
        padding: 0.6rem 1.2rem !important;
        width: auto !important;
    }}
    .stButton > button:hover, .stDownloadButton > button:hover {{
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        box-shadow: 0 6px 18px rgba(241, 196, 15, 0.4) !important;
        transform: translateY(-2px) !important;
    }}
    .stButton > button:active, .stDownloadButton > button:active {{
        transform: translateY(0px) !important;
    }}
    
    /* Metric Cards (Premium Glassmorphism / Slate style) */
    [data-testid="stMetric"] {{
        background-color: #1E293B !important;
        padding: 20px 25px !important;
        border-radius: 12px !important;
        border: 1px solid #334155 !important;
        border-top: 4px solid #F1C40F !important;
        box-shadow: 0 10px 20px -5px rgba(0,0,0,0.3) !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }}
    [data-testid="stMetric"]:hover {{
        transform: translateY(-4px) !important;
        box-shadow: 0 15px 25px -5px rgba(0,0,0,0.4) !important;
    }}
    
    /* Metric Text Overrides */
    [data-testid="stMetricLabel"] > div {{
        font-size: 1rem !important;
        font-weight: 600 !important;
        color: #94A3B8 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    [data-testid="stMetricValue"] {{
        color: #F8FAFC !important;
        font-size: 2.2rem !important;
        font-weight: 700 !important;
    }}
    
    /* Expander / Headers */
    .streamlit-expanderHeader {{
        font-weight: 600 !important;
        color: #F8FAFC !important;
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
    }}
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab"] {{
        background-color: transparent !important;
        color: #94A3B8 !important;
        padding: 10px 20px !important;
        font-size: 1rem !important;
        transition: all 0.2s ease !important;
    }}
    .stTabs [data-baseweb="tab"]:hover {{
        color: #F1C40F !important;
    }}
    .stTabs [aria-selected="true"] {{
        border-bottom-color: #F1C40F !important;
        border-bottom-width: 3px !important;
        color: #F1C40F !important;
        background-color: transparent !important;
        font-weight: bold !important;
    }}
    
    /* Inputs, Textareas, Selectboxes */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stTextArea>div>div>textarea {{
        background-color: #1E293B !important;
        color: #F8FAFC !important;
        border-radius: 8px !important;
        border: 1px solid #334155 !important;
        padding: 0.4rem 0.8rem !important;
    }}
    .stTextInput>div>div>input:focus, .stSelectbox>div>div>div:focus, .stTextArea>div>div>textarea:focus {{
        border-color: #F1C40F !important;
        box-shadow: 0 0 0 1px #F1C40F !important;
    }}
    
    /* Sidebar Styling Override */
    [data-testid="stSidebar"] {{
        background-color: #1E293B !important;
        border-right: 1px solid #334155 !important;
    }}
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1, 
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2, 
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3 {{
        color: #F1C40F !important;
    }}
    
    /* Dividers */
    hr {{
        border-color: #334155 !important;
    }}

    /* Dataframe Overrides */
    div[data-testid="stDataFrame"] {{
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
    }}
    </style>
    """, unsafe_allow_html=True)
