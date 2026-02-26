import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
import pandas as pd
from datetime import datetime


# =============================
# CONFIG
# =============================
st.set_page_config(
    page_title="Air Quality Intelligence Dashboard",
    page_icon="🌫",
    layout="centered"
)

API_KEY = ""   # 🔐 Replace with your key

# =============================
# PROFESSIONAL GLOBAL CSS
# =============================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to bottom right, #AFE6FA, #FFF4C7);
    font-family: 'Segoe UI', sans-serif;
}

h1, h2, h3 {
    color: #1E293B !important;
    font-weight: 700;
}

.subtitle {
    color: #64748B;
    font-size: 18px;
}

#.search-card {
 #   background: white;
#  padding: 25px;
 #   border-radius: 16px;
  #  border: 1px solid #E2E8F0;
   # box-shadow: 0 8px 25px rgba(0,0,0,0.05);
    #margin-bottom: 20px;
#}

.big-aqi {
    font-size: 90px;
    font-weight: 800;
    text-align: center;
}

.stButton > button {
    background-color: #0EA5E9 !important;
    color: white !important;
    border-radius: 10px !important;
    border: none !important;
    padding: 10px 20px !important;
    font-weight: 600 !important;
}

.stButton > button:hover {
    background-color: #0284C7 !important;
}

.stMetric {
    background: linear-gradient(to bottom right, #E0F2F1, #0EA5E9);
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
/* Grey search box */
.stTextInput > div > div > input {
    background-color: #f1f5f9 !important;   /* light grey */
    color: black !important;                /* typed text */
    border-radius: 10px !important;
    border: 1px solid #CBD5E1 !important;
    padding: 12px !important;
}

/* Placeholder grey */
.stTextInput > div > div > input::placeholder {
    color: #9ca3af !important;
}

/* Label grey */
.stTextInput label {
    color: #475569 !important;
    font-weight: 600;
}      
}
</style>
""", unsafe_allow_html=True)

# =============================
# HELPER FUNCTIONS
# =============================

def get_aqi_category(aqi):
    labels = {
        1: "Good",
        2: "Fair",
        3: "Moderate",
        4: "Poor",
        5: "Very Poor"
    }

    colors = {
        1: "#22c55e",
        2: "#84cc16",
        3: "#eab308",
        4: "#f97316",
        5: "#ef4444"
    }

    advisories = {
        1: "✅ Air quality is excellent. Enjoy outdoor activities!",
        2: "🙂 Acceptable air quality. Sensitive people should take care.",
        3: "😷 Sensitive groups should limit outdoor exposure.",
        4: "⚠️ Everyone may experience health effects.",
        5: "🚫 Avoid outdoor activities. Stay indoors."
    }

    return (
        labels.get(aqi, "Unknown"),
        colors.get(aqi, "#6b7280"),
        advisories.get(aqi, "No advisory available.")
    )

# =============================
# SESSION STATE
# =============================
if "page" not in st.session_state:
    st.session_state.page = "home"

if "lat" not in st.session_state:
    st.session_state.lat = None

if "lon" not in st.session_state:
    st.session_state.lon = None

if "location_name" not in st.session_state:
    st.session_state.location_name = ""

# =============================
# HOME PAGE
# =============================
if st.session_state.page == "home":

    st.title("🌫 Air Quality Intelligence")
    st.markdown(
        '<p class="subtitle">Check real-time air pollution levels worldwide</p>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="search-card">', unsafe_allow_html=True)
    st.subheader("🔎 Search by City")

    city = st.text_input(
    "Enter City Name",
    placeholder="e.g. Mumbai",
    label_visibility="visible"
)

    if st.button("Search AQI"):

        if not city or len(city) < 3:
            st.warning("Please enter at least 3 characters.")

        else:
            geo_url = (
                f"https://api.openweathermap.org/geo/1.0/direct"
                f"?q={city}&limit=1&appid={API_KEY}"
            )

            with st.spinner("Fetching location..."):
                try:
                    response = requests.get(geo_url)

                    if response.status_code == 200:
                        geo_data = response.json()

                        if geo_data:
                            st.session_state.lat = geo_data[0]["lat"]
                            st.session_state.lon = geo_data[0]["lon"]
                            st.session_state.location_name = geo_data[0]["name"]

                            st.session_state.page = "details"
                            st.rerun()
                        else:
                            st.error("City not found.")
                    else:
                        st.error("API Error.")
                except:
                    st.error("Network error.")

    st.markdown('</div>', unsafe_allow_html=True)

    # Map Selection
    st.subheader("🗺 Or Select from Map")

    m = folium.Map(
        location=[20.5937, 78.9629],
        zoom_start=4,
        tiles="CartoDB positron"
    )

    map_data = st_folium(m, height=450, use_container_width=True)

    if map_data and map_data.get("last_clicked"):
        st.session_state.lat = map_data["last_clicked"]["lat"]
        st.session_state.lon = map_data["last_clicked"]["lng"]
        st.session_state.location_name = "Selected Location"
        st.session_state.page = "details"
        st.rerun()

# =============================
# DETAILS PAGE
# =============================
elif st.session_state.page == "details":

    lat = st.session_state.lat
    lon = st.session_state.lon
    name = st.session_state.location_name

    st.title("📊 AQI Report")

    if lat and lon:

        aqi_url = (
            f"https://api.openweathermap.org/data/2.5/air_pollution"
            f"?lat={lat}&lon={lon}&appid={API_KEY}"
        )

        with st.spinner("Fetching AQI data..."):
            try:
                response = requests.get(aqi_url)

                if response.status_code == 200:
                    data = response.json()

                    if "list" in data:
                        aqi = data["list"][0]["main"]["aqi"]
                        components = data["list"][0]["components"]

                        category, color, advisory = get_aqi_category(aqi)

                        st.markdown(
                            f"<h2 style='text-align:center'>{name}</h2>",
                            unsafe_allow_html=True
                        )

                        st.markdown(
                            f"<div class='big-aqi' style='color:{color}'>{aqi}</div>",
                            unsafe_allow_html=True
                        )

                        st.markdown(
                            f"<p style='text-align:center; color:{color}; font-size:22px; font-weight:600;'>{category}</p>",
                            unsafe_allow_html=True
                        )

                        st.info(advisory)

                        st.divider()
                        st.subheader("🧪 Pollutant Breakdown")

                        col1, col2, col3 = st.columns(3)

                        with col1:
                            st.metric("PM2.5", round(components["pm2_5"], 1))
                            st.metric("PM10", round(components["pm10"], 1))

                        with col2:
                            st.metric("NO₂", round(components["no2"], 1))
                            st.metric("O₃", round(components["o3"], 1))

                        with col3:
                            st.metric("CO", round(components["co"], 1))
                            st.metric("SO₂", round(components["so2"], 1))


                        forecast_url = f"https://api.openweathermap.org/data/2.5/air_pollution/forecast?lat={lat}&lon={lon}&appid={API_KEY}"
                        forecast_data = requests.get(forecast_url).json()

                        st.subheader("Choose pollutant to view 5-day forecast")

                        option = st.selectbox(
                        "Pollutant",
                        ("PM 2.5", "PM10", "NO2","O3","SO2","CO"),
                        )

                        st.write("You selected:", option)
                        pollutant_info = {
                        "PM2.5": "Fine particles ≤2.5µm that penetrate deep into lungs.",
                        "PM10": "Particles ≤10µm affecting respiratory system.",
                        "NO2": "Nitrogen dioxide from vehicles & combustion.",
                        "O3": "Ground-level ozone formed via sunlight reactions.",
                        "CO": "Carbon monoxide reduces oxygen transport.",
                        "SO2": "Sulfur dioxide from fossil fuel burning."
                        }

                        st.write("",pollutant_info.get(option))

                        if option :

                            data = forecast_data["list"]

                            # Create empty lists
                            datetimes = []
                            values = []
                            key_map = {
                            "PM 2.5": "pm2_5",
                            "PM10": "pm10",
                            "NO2": "no2",
                            "O3": "o3",
                            "SO2": "so2",
                            "CO": "co"
                            }

                            # Loop through forecast entries
                            for entry in data:

                                # Convert timestamp
                                dt_object = datetime.fromtimestamp(entry["dt"])
                                datetimes.append(dt_object)

                                # Extract selected pollutant value
                                api_key_name = key_map[option]
                                pollutant_value = entry["components"][api_key_name]
                                values.append(pollutant_value)

                            # Create DataFrame manually
                            plot_df = pd.DataFrame({
                                "datetime": datetimes,
                                option: values
                            })

                        plot_df = plot_df.set_index("datetime")

                        st.line_chart(plot_df)


                    else:
                        st.error("AQI data unavailable.")

                else:
                    st.error("API request failed.")

            except:
                st.error("Network error.")

    st.divider()

    if st.button("⬅ Back to Home"):
        st.session_state.page = "home"
        st.rerun()
