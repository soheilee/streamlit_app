import base64
import streamlit as st
import os

def get_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def set_main_background(image_path):
    ext = os.path.splitext(image_path)[1][1:]  # 'jpg' or 'png'
    base64_img = get_base64(image_path)

    css = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background: url("data:image/{ext};base64,{base64_img}") no-repeat center center fixed;
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def display_app_header(main_txt,sub_txt,is_sidebar = False):
    """
    function to display major headers at user interface
    ----------
    main_txt: str -> the major text to be displayed
    sub_txt: str -> the minor text to be displayed 
    is_sidebar: bool -> check if its side panel or major panel
    """

    html_temp = f"""
    <h2 style = "color:#F74369; text_align:center; font-weight: bold;"> {main_txt} </h2>
    <p style = "color:#BB1D3F; text_align:center;"> {sub_txt} </p>
    </div>
    """
    if is_sidebar:
        st.sidebar.markdown(html_temp, unsafe_allow_html = True)
    else: 
        st.markdown(html_temp, unsafe_allow_html = True)