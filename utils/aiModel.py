import streamlit as st
import pandas as pd
from utils.model_loader import ModelLoader

class AiModel:
    """All widgets, callbacks & interaction live here."""

    def __init__(self):
        self.mod = st.session_state.get("ML") or ModelLoader()
        self.dp = None  # Optional, define if you're using it later
        self.setup_sidebar()
    
        st.session_state["DP"], st.session_state["ML"] = self.dp, self.mod

    def setup_sidebar(self):

        st.sidebar.title("Navigation / Actions")
        # ----- model load -----
        loc = st.sidebar.selectbox("Choose location",
                                   list(self.mod.model_folders.keys()))
        sub = st.sidebar.selectbox("Choose sub-model",
                                   ["NH4.pkl","COD.pkl","Ntot.pkl"])
        if st.sidebar.button("Load model"):
            try:
                self.mod.load(loc, sub)
                st.sidebar.success(f"Loaded {sub} for {loc}")
            except Exception as e:
                st.sidebar.error(str(e))