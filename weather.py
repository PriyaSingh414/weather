import requests
import streamlit as st
import base64
from datetime import datetime, timedelta

# OpenWeatherMap API key
api_key = "a6f81aff8e354cf14db2c448cbb27e5c"
hide_streamlit_cloud_elements = """
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    a[title="View source"] {display: none !important;}
    button[kind="icon"] {display: none !important;}
    </style>
"""
st.markdown(hide_streamlit_cloud_elements, unsafe_allow_html=True)

# Set background from local image
def set_bg_from_local(image_file):
    with open(image_file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(255, 255, 255, 0.7), rgba(255, 255, 255, 0.3)),
                        url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-attachment: fixed;
        }}
        h1, h2, h3, h4, h5, h6,
        .stButton > button,
        label,
        .stSelectbox,
        .stTextInput > div > div {{
            font-weight: bold !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Get user location by IP
def get_location_by_ip():
    try:
        res = requests.get("https://ipinfo.io/json")
        city = res.json().get("city")
        return city
    except:
        return None

# Fetch weather data
def weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    return response.json()

# Convert UTC timestamp to local time using timezone offset
def utc_to_local(utc_timestamp, offset_seconds):
    local_time = datetime.utcfromtimestamp(utc_timestamp) + timedelta(seconds=offset_seconds)
    return local_time.strftime('%I:%M %p')

# MAIN APP
def main():
    set_bg_from_local("images.jpg")
    st.title("🌦️Weather App")

    city = st.text_input("📍 Enter city name (or leave blank to detect your location)").strip()

    if not city:
        city = get_location_by_ip()
        if city:
            st.info(f"Auto-detected your city: {city}")
        else:
            st.warning("Unable to detect location. Please enter manually.")

    if city and st.button("🔍 Check Weather"):
        data = weather(city)

        if data.get("cod") == 200:
            offset = data["timezone"]

            # Main Info
            st.subheader(f"📍 Weather in {data['name']}, {data['sys']['country']}")
            col1, col2 = st.columns(2)

            with col1:
                st.metric("🌡 Temperature", f"{data['main']['temp']} °C", f"Feels like {data['main']['feels_like']} °C")
                st.metric("💧 Humidity", f"{data['main']['humidity']}%")
                st.metric("🌬 Wind Speed", f"{data['wind']['speed']} m/s")
                st.metric("🔽 Pressure", f"{data['main']['pressure']} hPa")

            with col2:
                st.write("☀️ **Sunrise:**", utc_to_local(data['sys']['sunrise'], offset))
                st.write("🌇 **Sunset:**", utc_to_local(data['sys']['sunset'], offset))
                st.write("🌥 **Condition:**", data['weather'][0]['description'].capitalize())
                icon_url = f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"
                st.image(icon_url, width=100)

            # Footer
            last_updated = utc_to_local(data['dt'], offset)
            st.caption(f"🕒 Last updated: {last_updated}")
        else:
            st.error("❌ City not found. Please check the name and try again.")

if __name__ == "__main__":
    main()
