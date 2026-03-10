import streamlit as st
from pages.home import show_home
from pages.dashboard import show_dashboard

st.set_page_config(
    page_title="Air Quality Intelligence",
    page_icon="🌫",
    layout="wide"
)


if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    show_home()

elif st.session_state.page == "dashboard":
    show_dashboard()
