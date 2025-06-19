import asyncio
from weather_tool import WeatherTool

async def test_weather():
    weather_tool = WeatherTool(api_key="3fa75fd7b40144c593f92101251806")
    result = await weather_tool.get_weather("New York", "imperial", 2)
    print(result)

if __name__ == "__main__":
    asyncio.run(test_weather())
