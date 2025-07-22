import streamlit as st
from utils.background_style import *

# Ensure session keys are initialized
if "finalized_files" not in st.session_state:
    st.session_state.finalized_files = {}

if "processed_files" not in st.session_state:
    st.session_state.processed_files = {}

# Set main background
set_main_background("assets/home_background.png")


st.title("🤖 AI Model Application")
st.write(f"Smart and Clean AI Product")
