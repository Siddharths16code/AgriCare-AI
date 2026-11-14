
import requests


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


def get_coordinates(city):

    try:
        response = requests.get(
            GEOCODING_URL,
            params={
                "name": city,
                "count": 1,
                "language": "en",
                "format": "json"
            },
            timeout=10
        )

        response.raise_for_status()
        results = response.json().get("results", [])

        if not results:
            return None, "Location not found. Please check the city name."

        location = results[0]

        return {
            "name": location["name"],
            "country": location.get("country", ""),
            "latitude": location["latitude"],
            "longitude": location["longitude"]
        }, None

    except requests.RequestException as error:
        return None, f"Location service error: {error}"


def get_weather(city):

    location, error = get_coordinates(city)

    if error:
        return None, error

    try:
        response = requests.get(
            WEATHER_URL,
            params={
                "latitude": location["latitude"],
                "longitude": location["longitude"],
                "current": [
                    "temperature_2m",
                    "relative_humidity_2m",
                    "precipitation",
                    "wind_speed_10m",
                    "weather_code"
                ],
                "daily": [
                    "temperature_2m_max",
                    "temperature_2m_min",
                    "precipitation_probability_max",
                    "precipitation_sum"
                ],
                "timezone": "auto",
                "forecast_days": 5
            },
            timeout=15
        )

        response.raise_for_status()
        data = response.json()

        return {
            "location": location,
            "current": data["current"],
            "daily": data["daily"],
            "timezone": data.get("timezone", "auto")
        }, None

    except (requests.RequestException, KeyError, ValueError) as error:
        return None, f"Weather service error: {error}"


def get_crop_recommendations(weather):

    current = weather["current"]
    daily = weather["daily"]

    recommendations = []

    temperature = current["temperature_2m"]
    humidity = current["relative_humidity_2m"]
    rainfall = current["precipitation"]

    max_rain_probability = max(
        daily["precipitation_probability_max"]
    )

    if temperature >= 35:
        recommendations.append(
            "High temperature detected. Monitor soil moisture "
            "and avoid unnecessary water stress."
        )

    if humidity >= 85:
        recommendations.append(
            "High humidity may favour fungal diseases. "
            "Inspect potato leaves regularly for disease symptoms."
        )

    if rainfall >= 10 or max_rain_probability >= 70:
        recommendations.append(
            "Rainfall risk is elevated. Avoid unnecessary irrigation "
            "and check field drainage."
        )

    if temperature <= 5:
        recommendations.append(
            "Low temperature detected. Monitor the crop for cold or frost damage."
        )

    if not recommendations:
        recommendations.append(
            "No major weather-related risk detected from the current "
            "weather indicators. Continue regular crop monitoring."
        )

    return recommendations
