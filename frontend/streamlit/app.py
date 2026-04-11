# ============================================
# MAIN STREAMLIT APPLICATION
# Tesla Financial Intelligence RAG System
# ============================================

import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from frontend.streamlit.components.sidebar import render_sidebar
from frontend.streamlit.components.chat import render_chat
from frontend.streamlit.config import APP_TITLE, APP_ICON, APP_SUBTITLE


# --- Page Configuration ---
st.set_page_config(
    page_title            = APP_TITLE,
    page_icon             = APP_ICON,
    layout                = "wide",
    initial_sidebar_state = "expanded",
)


# --- Custom CSS (Light Tesla Theme) ---
st.markdown("""
    <style>
        /* ===== MAIN BACKGROUND ===== */
        .stApp {
            background-color: #F5F5F5;
            color: #1A1A1A;
        }

        /* ===== SIDEBAR ===== */
        [data-testid="stSidebar"] {
            background-color: #FFFFFF;
            border-right: 3px solid #2563EB;
            box-shadow: 2px 0 10px rgba(0,0,0,0.08);
        }

        /* ===== HEADER ===== */
        .main-header {
            background: linear-gradient(135deg, #E31937 0%, #B01228 100%);
            padding: 2rem;
            border-radius: 16px;
            margin-bottom: 1.5rem;
            text-align: center;
            box-shadow: 0 8px 25px rgba(227, 25, 55, 0.25);
        }

        /* ===== CHAT MESSAGES ===== */
        [data-testid="stChatMessage"] {
            background-color: #FFFFFF;
            border-radius: 16px;
            padding: 1rem;
            margin-bottom: 1rem;
            border: 1px solid #EEEEEE;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        }

        /* ===== CHAT INPUT ===== */
        [data-testid="stChatInput"] {
            background-color: #FFFFFF;
            border: 2px solid #E31937 !important;
            border-radius: 16px;
            box-shadow: 0 4px 12px rgba(227, 25, 55, 0.15);
        }

        /* ===== BUTTONS ===== */
        .stButton > button {
            background-color: #FFFFFF;
            color: #333333;
            border: 1px solid #E0E0E0;
            border-radius: 8px;
            font-size: 0.78rem;
            text-align: left;
            transition: all 0.2s ease;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }

        .stButton > button:hover {
            background-color: #E31937;
            color: white !important;
            border-color: #E31937;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(227, 25, 55, 0.25);
        }

        /* ===== METRICS ===== */
        [data-testid="stMetricValue"] {
            color: #E31937;
            font-size: 2rem;
            font-weight: 800;
        }

        [data-testid="stMetricLabel"] {
            color: #888888;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        /* ===== METRIC CONTAINER ===== */
        [data-testid="stMetric"] {
            background: #F8F8F8;
            border-radius: 10px;
            padding: 0.5rem;
            border: 1px solid #EEEEEE;
        }

        /* ===== EXPANDER ===== */
        [data-testid="stExpander"] {
            background-color: #FFFFFF;
            border: 1px solid #EEEEEE;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }

        /* ===== SUCCESS BOX ===== */
        [data-testid="stAlert"] {
            border-radius: 10px;
        }

        /* ===== DIVIDER ===== */
        hr {
            border-color: #F0F0F0;
            margin: 1rem 0;
        }

        /* ===== SCROLLBAR ===== */
        ::-webkit-scrollbar {
            width: 5px;
        }
        ::-webkit-scrollbar-track {
            background: #F5F5F5;
        }
        ::-webkit-scrollbar-thumb {
            background: #E31937;
            border-radius: 10px;
        }

        /* ===== HIDE STREAMLIT BRANDING ===== */
        #MainMenu  {visibility: hidden;}
        footer     {visibility: hidden;}
        header     {visibility: hidden;}

        /* ===== CODE BLOCKS ===== */
        code {
            background-color: #FFF0F2;
            color: #E31937;
            padding: 0.15rem 0.4rem;
            border-radius: 4px;
            font-size: 0.85rem;
        }

        /* ===== SELECTBOX ===== */
        [data-testid="stSelectbox"] > div {
            border-radius: 8px;
        }

        /* ===== SLIDER ===== */
        [data-testid="stSlider"] {
            padding: 0.5rem 0;
        }

        /* ===== MARKDOWN TEXT ===== */
        .stMarkdown p {
            color: #333333;
            line-height: 1.6;
        }

        /* ===== CAPTION ===== */
        .stCaption {
            color: #999999 !important;
        }
    </style>
""", unsafe_allow_html=True)


# --- Header ---
st.markdown(f"""
    <div class='main-header'>
        <h1 style='
            color: white;
            font-size: 2.2rem;
            margin: 0;
            letter-spacing: 3px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.2);
            font-weight: 800;
        '>
            {APP_ICON} {APP_TITLE.upper()}
        </h1>
        <p style='
            color: rgba(255,255,255,0.9);
            margin: 0.6rem 0 0 0;
            font-size: 1rem;
            letter-spacing: 2px;
            font-weight: 300;
        '>
            {APP_SUBTITLE}
        </p>
    </div>
""", unsafe_allow_html=True)


# --- Render Components ---
render_sidebar()
render_chat()