import streamlit as st
from services.weather_api import get_coordinates

def show_home():

    city = st.text_input("Enter City")

    if st.button("Search AQI"):

        with st.spinner("Fetching location..."):

            lat, lon, name = get_coordinates(city)

            if lat is not None:

                st.session_state.lat = lat
                st.session_state.lon = lon
                st.session_state.location_name = name
                st.session_state.page = "details"

                st.rerun()

            else:
                st.error("City not found or API error.")
