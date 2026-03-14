import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
import requests
import folium
from streamlit_folium import st_folium


# =============================
# CONFIG
# =============================
st.set_page_config(
    page_title="Air Quality Intelligence Dashboard",
    page_icon="🌫",
    layout="wide"
)


API_KEY = st.secrets["API_KEY"]

# =============================
# GLOBAL CSS
# =============================
st.markdown("""
<style>
.stApp {                                                                                       
    background: linear-gradient(to bottom right, #AFE6FA, #FFF4C7);
    font-family: 'Segoe UI', sans-serif;
}

h1,h2,h3 {
    color: #1E293B !important;
   font-weight: 700;
}

.subtitle {
    color: #64748B;
    font-size: 18px;
}
            
.stTextInput > div > div > input {
    background-color: #f1f5f9 !important; 
    color: black !important;                
    border-radius: 10px !important;
}
.stTextInput > div > div >input::placeholder {
    color:  #64748B !important;
    opacity: 100;
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

.stTextInput label {
    color: #475569 !important;
     font-weight: 600;
 }   
</style>
""", unsafe_allow_html=True)

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
    st.subheader("🔎 Search by City")

    city = st.text_input(
    "Enter City Name",
    placeholder="e.g. Mumbai",
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

    # Map Selection
    st.subheader("🗺 Or Select from Map")

    m = folium.Map(
        location=[20.5937, 78.9629],
        zoom_start=4,
        tiles="CartoDB positron"
    )

    map_data = st_folium(m, height=450, width='content')
    try:
        if map_data and map_data.get("last_clicked"):
            st.session_state.lat = map_data["last_clicked"]["lat"]
            st.session_state.lon = map_data["last_clicked"]["lng"]
            st.session_state.location_name = "Selected Location"
            st.session_state.page = "details"
            st.rerun()
    except:
        st.error("Network error.")

# =============================
# DETAILS PAGE
# =============================
elif st.session_state.page == "details":
    st_autorefresh(interval=30000, key="refresh")

    st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    </style>
    """, unsafe_allow_html=True)

    lat = st.session_state.lat
    lon = st.session_state.lon
    name = st.session_state.location_name

    if lat and lon:

        aqi_url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
        forecast_url = f"https://api.openweathermap.org/data/2.5/air_pollution/forecast?lat={lat}&lon={lon}&appid={API_KEY}"

        with st.spinner("Fetching AQI data..."):
            current = requests.get(aqi_url).json()
            forecast = requests.get(forecast_url).json()

        if "list" in current:

            aqi = current["list"][0]["main"]["aqi"]
            components = current["list"][0]["components"]

            aqi_scaled = aqi

            st.markdown(
                f"<h2 style='color:white;'>AIR QUALITY DASHBOARD | {name.upper()} | {datetime.now().strftime('%A, %b %d, %Y | %I:%M %p')}</h2>",
                unsafe_allow_html=True
            )

            left, right = st.columns([1,2])

            # ---------------- GAUGE ----------------
            
            with left:
               
                gauge = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=aqi,
                    title={'text': "CURRENT AQI"},
                    gauge={
                        'axis': {'range': [0, 5]},
                        'bar': {'color': "white"},
                        'steps': [
                            {'range': [0, 1], 'color': "#00e400"},
                            {'range': [1, 2], 'color': "#9cff00"},
                            {'range': [2, 3], 'color': "#ffff00"},
                            {'range': [3, 4], 'color': "#ff7e00"},
                            {'range': [4, 5], 'color': "#ff0000"},
                        ],
                    }
                
                ))
                st.markdown("""<div style=
                            "margin-top:60px;
                            ">
                            """, unsafe_allow_html=True)
                gauge.update_layout(
                    paper_bgcolor="#1c2333",
                    font={'color': "white"},
                    height=250,  
                    margin=dict(l=10, r=10, t=50, b=10) 
                )
                st.plotly_chart(gauge, width='content')
                st.markdown("""
                <div style="
                background:#1c2333;
                padding:18px;
                border-radius:30px;
                color:white;
                font-size:14px;
                margin-top:10px;
                margin-bottom:0px;    
                line-height:1.1;    
                ">

                <h4 style="margin-bottom:10px;">AQI Scale (0–5)</h4>

                <div style="display:flex;align-items:center;margin-bottom:6px;">
                <span style="width:12px;height:12px;background:#00e400;border-radius:50%;display:inline-block;margin-right:8px;"></span>
                0 – 0.5  →  Good (0–50)
                </div>

                <div style="display:flex;align-items:center;margin-bottom:6px;">
                <span style="width:12px;height:12px;background:#9cff00;border-radius:50%;display:inline-block;margin-right:8px;"></span>
                0.5 – 1  →  Satisfactory (51–100)
                </div>

                <div style="display:flex;align-items:center;margin-bottom:6px;">
                <span style="width:12px;height:12px;background:#ffff00;border-radius:50%;display:inline-block;margin-right:8px;"></span>
                1 – 2  →  Moderate (101–200)
                </div>

                <div style="display:flex;align-items:center;margin-bottom:6px;">
                <span style="width:12px;height:12px;background:#ff7e00;border-radius:50%;display:inline-block;margin-right:8px;"></span>
                2 – 3  →  Poor (201–300)
                </div>

                <div style="display:flex;align-items:center;">
                <span style="width:12px;height:12px;background:#ff0000;border-radius:50%;display:inline-block;margin-right:8px;"></span>
                3 – 5  →  Severe (301–500)
                </div>

                </div>
                """, unsafe_allow_html=True)

            # ---------------- POLLUTANT CARDS ----------------
            with right:
                st.markdown("### KEY POLLUTANTS:-")

                pollutant_map = {
                    "PM2.5": components["pm2_5"],
                    "PM10": components["pm10"],
                    "NO2": components["no2"],
                    "SO2": components["so2"],
                    "CO": components["co"],
                    "O3": components["o3"],
                }

                cols = st.columns(3)
                POLLUTANT_API_KEYS = {
                "PM2.5": "pm2_5",
                "PM10":  "pm10",
                "NO2":   "no2",
                "SO2":   "so2",
                "CO":    "co",
                "O3":    "o3",
                 }
                for i, (key, value) in enumerate(pollutant_map.items()):
                    with cols[i % 3]:

                        trend_vals = []
                        times = []
                    
                        for entry in forecast["list"][:10]:
                            times.append(datetime.fromtimestamp(entry["dt"]))
                            trend_vals.append(entry["components"][POLLUTANT_API_KEYS[key]])
                        fig = go.Figure()
                        fig.add_trace(go.Scatter(
                            x=times,
                            y=trend_vals,
                            mode='lines',
                            line=dict(color='#ffa500'),
                            showlegend=False
                        ))

                        fig.update_layout(
                            height=120,
                            margin=dict(l=0,r=0,t=0,b=0),
                            font=dict(color="white")
                        )

                        st.markdown(f"""
                        <div style="
                            background:#1c2333;
                            padding:15px;
                        ">
                            <div style="color:white; font-size:18px;">{key}</div>
                            <div style="color:white; font-size:28px; font-weight:bold;">
                                {round(value,2)}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        st.plotly_chart(fig, width='content')

            # ---------------- 5 DAY FORECAST ----------------
            st.markdown("## 5-DAY AIR QUALITY FORECAST")

            df_list = []
            for entry in forecast["list"]:
                row = {
                    "Day": datetime.fromtimestamp(entry["dt"]),
                    "PM2.5": entry["components"]["pm2_5"],
                    "PM10": entry["components"]["pm10"],
                    "NO2": entry["components"]["no2"],
                    "SO2": entry["components"]["so2"],
                    "CO": entry["components"]["co"],
                    "O3": entry["components"]["o3"],
                }
                df_list.append(row)

            df = pd.DataFrame(df_list)

            fig2 = go.Figure()

            colors = {
                "AQI": "orange",
                "PM2.5": "lightblue",
                "PM10": "cyan",
                "NO2": "red",
                "SO2": "green",
                "CO": "yellow",
                "O3": "purple"
            }

            for col in df.columns[1:]:
                fig2.add_trace(go.Scatter(
                    x=df["Day"],
                    y=df[col],
                    mode="lines",
                    name=col,
                    line=dict(color=colors[col])
                ))

            fig2.update_layout(
                font=dict(color="white"),
                height=500
            )

            st.markdown("""
            <div style="
            background:#1c2333;
            padding:15px;
            box-shadow:0 0 10px rgba(0,0,0,0.4);
            ">
            """, unsafe_allow_html=True)

            st.plotly_chart(fig2, width='stretch')
    if st.button("⬅ Back to Home"):
        st.session_state.page = "home"
        st.rerun()

