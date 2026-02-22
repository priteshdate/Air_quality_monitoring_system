import streamlit as st
import time
# Page config MUST be first Streamlit command
st.set_page_config(page_title="Welcome Page", page_icon="🌐", layout="centered")



# Custom CSS
st.markdown(
    """
    <style>
    .welcome-text {
        color: #1E90FF;
        font-size: 48px;
        font-weight: bold;
        text-align: center;
        margin-top: 50px;
    }
    .city-header {
        font-size: 32px;
        font-weight: bold;
        color: #1E90FF;
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Session state
if "page" not in st.session_state:
    st.session_state.page = "home"

# Home page
if st.session_state.page == "home":
    st.markdown('<div class="welcome-text">Welcome</div>', unsafe_allow_html=True)

    city = st.selectbox(
        "Select city to monitor the air quality:",
        ["-- Select city --", "Delhi", "Mumbai"]
    )

    if city != "-- Select city --":
        with st.spinner("Loading..."):
            time.sleep(2)

        st.session_state.page = "city"
        st.session_state.selected_city = city
        st.rerun()

# City page
elif st.session_state.page == "city":
    st.markdown(
        f'<div class="city-header">{st.session_state.selected_city}</div>',
        unsafe_allow_html=True
    )
    st.write(f"Now monitoring air quality for **{st.session_state.selected_city}**.")

    if st.button("⬅ Back"):
        st.session_state.page = "home"
        st.rerun()