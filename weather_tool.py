import requests
from typing import Dict, Any
import os

class WeatherTool:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "http://api.weatherapi.com/v1"
    
    async def get_weather(self, location: str, units: str = "metric", forecast_days: int = 1) -> Dict[str, Any]:
        url = f"{self.base_url}/forecast.json"
        params = {
            "key": self.api_key,
            "q": location,
            "days": min(forecast_days, 10),
            "aqi": "yes",
            "alerts": "yes"
        }
        try:
            response = requests.get(url, params=params)
            if response.status_code == 400:
                return {"error": f"Location '{location}' not found"}
            elif response.status_code == 401:
                return {"error": "Invalid API key"}
            elif response.status_code == 403:
                return {"error": "API key quota exceeded"}
            response.raise_for_status()
            data = response.json()
            return self._format_response(data, units)
        except requests.RequestException as e:
            return {"error": f"Failed to fetch weather data: {str(e)}"}
    
    def _format_response(self, data: Dict, units: str) -> Dict[str, Any]:
        current = data["current"]
        location = data["location"]
        # Temperature conversion
        if units == "imperial":
            temp = current["temp_f"]
            feels_like = current["feelslike_f"]
            temp_unit = "°F"
            wind_speed = current["wind_mph"]
            wind_unit = "mph"
            visibility = current["vis_miles"]
            vis_unit = "miles"
        elif units == "kelvin":
            temp = current["temp_c"] + 273.15
            feels_like = current["feelslike_c"] + 273.15
            temp_unit = "K"
            wind_speed = current["wind_kph"]
            wind_unit = "km/h"
            visibility = current["vis_km"]
            vis_unit = "km"
        else:  # metric (default)
            temp = current["temp_c"]
            feels_like = current["feelslike_c"]
            temp_unit = "°C"
            wind_speed = current["wind_kph"]
            wind_unit = "km/h"
            visibility = current["vis_km"]
            vis_unit = "km"
        result = {
            "location": f"{location['name']}, {location['region']}, {location['country']}",
            "current": {
                "temperature": round(temp, 1),
                "temperature_unit": temp_unit,
                "feels_like": round(feels_like, 1),
                "humidity": current["humidity"],
                "description": current["condition"]["text"],
                "wind_speed": wind_speed,
                "wind_unit": wind_unit,
                "wind_direction": current["wind_dir"],
                "pressure": current["pressure_mb"],
                "uv_index": current["uv"],
                "visibility": visibility,
                "visibility_unit": vis_unit,
                "cloud_cover": current["cloud"],
                "last_updated": current["last_updated"]
            },
            "forecast": []
        }
        # Add forecast days
        if "forecast" in data:
            for day in data["forecast"]["forecastday"]:
                day_data = day["day"]
                if units == "imperial":
                    high_temp = day_data["maxtemp_f"]
                    low_temp = day_data["mintemp_f"]
                elif units == "kelvin":
                    high_temp = day_data["maxtemp_c"] + 273.15
                    low_temp = day_data["mintemp_c"] + 273.15
                else:
                    high_temp = day_data["maxtemp_c"]
                    low_temp = day_data["mintemp_c"]
                result["forecast"].append({
                    "date": day["date"],
                    "high": round(high_temp, 1),
                    "low": round(low_temp, 1),
                    "temperature_unit": temp_unit,
                    "description": day_data["condition"]["text"],
                    "rain_chance": day_data["daily_chance_of_rain"],
                    "snow_chance": day_data["daily_chance_of_snow"],
                    "max_wind": day_data["maxwind_kph"] if units == "metric" else day_data["maxwind_mph"],
                    "avg_humidity": day_data["avghumidity"],
                    "uv_index": day_data["uv"]
                })
        return result

async def main(location: str, units: str = "metric", forecast_days: int = 1, api_key: str = None):
    key = api_key or os.environ.get("WEATHER_API_KEY")
    if not key:
        return {"error": "API key required"}
    tool = WeatherTool(api_key=key)
    return await tool.get_weather(location, units, forecast_days)
