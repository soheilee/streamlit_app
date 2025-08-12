import streamlit as st
import pandas as pd
import io
from utils.background_style import *

class SidebarManager:
    def __init__(self ):
        self.setup_sidebar()

    def setup_sidebar(self):

        # Number of files input
        if "num_files" not in st.session_state:
            st.session_state.num_files = 1
        st.sidebar.number_input(
            "How many files will you upload?",
            min_value=1,
            step=1,
            key="num_files"
        )

        # Page navigation radio
        pages = [f"File {i+1}" for i in range(st.session_state.num_files)]
        st.session_state.current_page = st.sidebar.radio("Select a page:", pages, key="page_radio")

        # Merge button
        if st.sidebar.button("Merge Finalized Files Horizontally") and st.session_state.get("finalized_files"):
            self.merge_and_download(st.session_state.finalized_files)
        if st.sidebar.button("Merge Finalized Files Vertically") and st.session_state.get("finalized_files"):
            self.merge_and_download(st.session_state.finalized_files)

    def merge_and_download(self, files_dict):
        merged_df = pd.concat(files_dict.values(), axis=1)
        st.session_state.processed_files["merged"] = merged_df
        st.sidebar.success("Finalized files merged successfully!")

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            merged_df.to_excel(writer, index=False, sheet_name='MergedData')
        output.seek(0)

        st.sidebar.download_button(
            label="Download Merged File",
            data=output,
            file_name="merged_file.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
