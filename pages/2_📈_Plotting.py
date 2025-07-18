import streamlit as st
from utils.background_style import *
from utils.scatter_plot import N2OPlotter

# Ensure session keys are initialized
if "finalized_files" not in st.session_state:
    st.session_state.finalized_files = {}

if "processed_files" not in st.session_state:
    st.session_state.processed_files = {}

# Set main background
set_main_background("assets/main_bg.png")


st.title("🛠️ Data Illustration Application")
st.write(f"Explore, Visualise, and Unlock your data’s potential.")


N2OPlotter()
