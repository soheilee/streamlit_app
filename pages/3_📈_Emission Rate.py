import streamlit as st
from utils.background_style import *
from utils.scatter_plot import N2OPlotter

# Ensure session keys are initialized
if "finalized_files" not in st.session_state:
    st.session_state.finalized_files = {}

if "processed_files" not in st.session_state:
    st.session_state.processed_files = {}

# Set main background
set_main_background("assets/vis_bg.png")

# Add readable text box style
st.markdown("""
    <style>
    .custom-textbox {
        
        padding: 20px;
        border-radius: 10px;
        color: black;
    }
    </style>
""", unsafe_allow_html=True)

# Use styled div to show title + text
st.markdown('<div class="custom-textbox"><h1>🛠️ Emission Rate Calculcation</h1>'
            '<p>Explore and visualise your data.</p></div>',
            unsafe_allow_html=True)



N2OPlotter()
