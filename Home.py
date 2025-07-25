import streamlit as st
from utils.background_style import *

# Set background image
set_main_background("assets/home_background.png")

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
st.markdown('<div class="custom-textbox"><h1>Welcome to Variolytics App Suite</h1>'
            '<p>Use the sidebar to navigate between the apps.</p></div>',
            unsafe_allow_html=True)