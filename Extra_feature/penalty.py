import streamlit as st
def show_penalty(aqi, components):
    st.subheader("Penalty Framework India")
    st.markdown("""
            <style>
            table {
                border-collapse: collapse;
                width: 100%;
                font-family: 'Segoe UI', sans-serif;
            
            }
            th {
                background-color: #2d6a4f;
                color: white;
                padding: 12px;
                text-align: center;
            }
            td {
                padding: 10px;
                border: 1px solid #000 !important;
                text-align: center;
                color:Black;
                background-color: #FFFFFF
            }
           
            </style>

            <table>
            <tr>
                <th>AQI Range</th>
                <th>Category</th>
                <th>Health Impact</th>
                <th>Daily Penalty</th>
            </tr>
            <tr>
                <td style="background-color:#00e400; font-weight:bold;">0 – 50</td>
                <td>Good</td>
                <td>No health impact</td>
                <td>None</td>
            </tr>
            <tr>
                <td style="background-color:#9cff00; font-weight:bold;">1 – 100</td>
                <td>Satisfactory</td>
                <td>Minor discomfort for sensitive groups</td>
                <td>None</td>
            </tr>
            <tr>
                <td style="background-color:#ffff00; font-weight:bold;">101 – 200</td>
                <td>Moderate</td>
                <td>Breathing discomfort for sensitive people</td>
                <td>Warning issued</td>
            </tr>
            <tr>
                <td style="background-color:#ff7e00; font-weight:bold;">201 – 300</td>
                <td>Poor</td>
                <td>Breathing discomfort for most people</td>
                <td>Rs. 25 lakh/day</td>
            </tr>
            <tr>
                <td style="background-color:#ff0000; font-weight:bold;">301 – 400</td>
                <td>Very Poor</td>
                <td>Respiratory illness on prolonged exposure</td>
                <td>Rs. 75 lakh/day</td>
            </tr>
            <tr>
                <td style="background-color:violet; font-weight:bold;">401 – 500</td>
                <td>Severe</td>
                <td>Serious risk; affects healthy people</td>
                <td>Rs. 2 crore/day</td>
            </tr>
            </table>
            """, unsafe_allow_html=True)
            
    if aqi == 1:
        category = "Good"
        health_impact = "No health impact"
        daily_penalty = "None"
        color = "#00e400"
    elif aqi == 2:
        category = "Satisfactory"
        health_impact = "Minor discomfort for sensitive groups"
        daily_penalty = "None"
        color = "#9cff00"
    elif aqi == 3:
        category = "Moderate"
        health_impact = "Breathing discomfort for sensitive people"
        daily_penalty = "Warning issued"
        color = "#ffff00"
    elif aqi == 4:
        category = "Poor"
        health_impact = "Breathing discomfort for most people"
        daily_penalty = "Rs. 25 lakh/day"
        color = "#ff7e00"
    elif aqi == 5:
        category = "Very Poor"
        health_impact = "Respiratory illness on prolonged exposure"
        daily_penalty = "Rs. 75 lakh/day"
        color = "#ff0000"
    elif any(comp > 500 for comp in components.values()):
        category = "Severe"
        health_impact = "Serious risk; affects healthy people"
        daily_penalty = "Rs. 2 crore/day"
        color = "#888"
    st.subheader(f"Penalty:  {daily_penalty}")

    st.markdown(f"""
            <div style="background-color:{color}; padding:15px; border-radius:10px; color:black; margin-bottom: 10px;">
                <b>Category:</b> {category} <br>
                <b>Health Impact:</b> {health_impact} <br>
                <b>Daily Penalty:</b> {daily_penalty}
               
            </div>
            """, unsafe_allow_html=True)
