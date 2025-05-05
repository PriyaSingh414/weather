import requests
import streamlit as st
import base64
# OpenWeatherMap API key
api_key = "a6f81aff8e354cf14db2c448cbb27e5c"
# URL of the background image


# Inject custom CSS to set the background image
def set_bg_from_local(image_file):
    with open(image_file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(255, 255, 255, 0.6), rgba(255, 255, 255, 0.3)),
                        url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            font-weight: bold !important;
        }}
        h1, h2, h3, h4, h5, h6,
        .stButton > button,
        label,
        .css-1cpxqw2,
        .stSelectbox,
        .stTextInput > div > div {{
            font-weight: bold !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
set_bg_from_local("images.jpg")
def weather(city):
    """Fetch weather data from OpenWeatherMap API."""
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    return response.json()

def main():
    st.title("Weather App")

    city = st.text_input("Enter city name")

    if city:
        if st.button("Submit"):
            data = weather(city)

            if data.get("cod") == 200:
                st.subheader(f"Weather in {data['name']}, {data['sys']['country']}")
                st.write(f"Temperature: {data['main']['temp']}°C")
                st.write(f"Humidity: {data['main']['humidity']}%")
                st.write(f"Weather: {data['weather'][0]['description'].capitalize()}")
                st.write(f"Wind Speed: {data['wind']['speed']} m/s")

                # Display weather icon
                icon_code = data['weather'][0]['icon']
                icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
                st.image(icon_url, width=100)
            else:
                st.error("City not found. Please check the name and try again.")

if __name__ == "__main__":
    main()
