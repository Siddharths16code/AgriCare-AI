
import streamlit as st
import pandas as pd
import plotly.express as px

from agricare.services.weather import (
    get_weather,
    get_crop_recommendations
)


def get_weather_description(code):

    descriptions = {
        0: "Clear Sky ☀️",
        1: "Mainly Clear 🌤️",
        2: "Partly Cloudy ⛅",
        3: "Overcast ☁️",
        45: "Fog 🌫️",
        48: "Depositing Rime Fog 🌫️",
        51: "Light Drizzle 🌦️",
        53: "Moderate Drizzle 🌦️",
        55: "Dense Drizzle 🌧️",
        61: "Slight Rain 🌧️",
        63: "Moderate Rain 🌧️",
        65: "Heavy Rain 🌧️",
        71: "Light Snow ❄️",
        73: "Moderate Snow ❄️",
        75: "Heavy Snow ❄️",
        80: "Rain Showers 🌦️",
        81: "Moderate Rain Showers 🌧️",
        82: "Heavy Rain Showers 🌧️",
        95: "Thunderstorm ⛈️"
    }

    return descriptions.get(code, "Variable Weather")


def render_weather_page(user):

    st.markdown(
        '<div class="main-title">Weather & Crop Health 🌦️</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Weather forecasts and farming recommendations for your location.</div>',
        unsafe_allow_html=True
    )

    st.write("")

    # Location input

    city = st.text_input(
        "📍 Enter your Village / City",
        value="Sonipat",
        placeholder="Example: Sonipat, Palwal, Rohtak"
    )

    if st.button("Get Weather Update", use_container_width=True):

        if not city.strip():
            st.warning("Please enter a location.")
            return

        with st.spinner("Fetching weather information..."):

            weather, error = get_weather(city.strip())

        if error:
            st.error(error)
            return

        st.session_state["weather_data"] = weather
        st.session_state["weather_city"] = city.strip()

    weather = st.session_state.get("weather_data")

    if not weather:
        st.info("Enter your location and click Get Weather Update.")
        return

    current = weather["current"]
    daily = weather["daily"]
    location = weather["location"]

    st.divider()

    st.subheader(
        f"Current Weather — {location['name']}, {location['country']}"
    )

    weather_description = get_weather_description(
        current["weather_code"]
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Temperature",
        f"{current['temperature_2m']} °C"
    )

    col2.metric(
        "Humidity",
        f"{current['relative_humidity_2m']} %"
    )

    col3.metric(
        "Rainfall",
        f"{current['precipitation']} mm"
    )

    col4.metric(
        "Wind Speed",
        f"{current['wind_speed_10m']} km/h"
    )

    st.info(f"Current Conditions: {weather_description}")

    st.divider()

    # Five-day forecast

    st.subheader("📅 5-Day Weather Forecast")

    forecast_df = pd.DataFrame({
        "Date": daily["time"],
        "Maximum Temperature (°C)": daily["temperature_2m_max"],
        "Minimum Temperature (°C)": daily["temperature_2m_min"],
        "Rain Probability (%)": daily["precipitation_probability_max"],
        "Rainfall (mm)": daily["precipitation_sum"]
    })

    st.dataframe(
        forecast_df,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("🌡️ Temperature Forecast")

    temperature_df = forecast_df.melt(
        id_vars=["Date"],
        value_vars=[
            "Maximum Temperature (°C)",
            "Minimum Temperature (°C)"
        ],
        var_name="Temperature Type",
        value_name="Temperature"
    )

    fig = px.line(
        temperature_df,
        x="Date",
        y="Temperature",
        color="Temperature Type",
        markers=True,
        title="Maximum and Minimum Temperature"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Crop health recommendations

    st.subheader("🌱 Crop Health Recommendations")

    recommendations = get_crop_recommendations(weather)

    for recommendation in recommendations:
        st.success(f"🌿 {recommendation}")

    st.caption(
        "Note: These recommendations are general weather-based guidance. "
        "Actual crop management decisions should consider field conditions "
        "and advice from an agricultural expert."
    )
