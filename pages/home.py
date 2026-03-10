import streamlit as st
from services.weather_api import get_coordinates

def show_home():

    st.title("🌫 Air Quality Intelligence")

    city = st.text_input("Enter City")

    if st.button("Search AQI"):

        lat, lon, name = get_coordinates(city)

        st.session_state.lat = lat
        st.session_state.lon = lon
        st.session_state.location_name = name
        st.session_state.page = "dashboard"
        st.rerun()
