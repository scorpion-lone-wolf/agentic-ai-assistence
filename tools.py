def get_current_temperature(city: str) -> str:
    """
    Fake weather tool for learning tool calling.
    """

    temperatures = {
        "delhi": "33°C",
        "mumbai": "29°C",
        "bangalore": "24°C",
        "london": "18°C",
    }

    return temperatures.get(city.lower(), f"No temperature data available for {city}")
