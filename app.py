import streamlit as st
from utils.background_style import *
from utils.sidebar import SidebarManager
from utils.file_page_handler import FilePageHandler

# Ensure session keys are initialized
if "finalized_files" not in st.session_state:
    st.session_state.finalized_files = {}

if "processed_files" not in st.session_state:
    st.session_state.processed_files = {}

# Set main background
set_main_background("assets/main_bg.png")


# Load sidebar
SidebarManager()


st.title("Data Quality Application")
st.write(f"Clean, describe, visualise and select data for AI models.")


display_app_header(main_txt = "Step 1",
                       sub_txt= "All Sheets Combining &nbsp;&nbsp;&nbsp;+&nbsp;&nbsp;&nbsp;    Date-Time Cleaning",
                       is_sidebar=False)


# Main content

index = int(st.session_state.current_page.split(" ")[1]) - 1
FilePageHandler(index)
