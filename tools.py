# function
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


# =========================================================================
# Tool definition sent to LLM (By this LLM will know what all tools are available)
# =========================================================================
tool_schemas = [
    {
        "type": "function",
        "function": {
            "name": "get_current_temperature",
            "description": "Fetch the current temperature of a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The name of the city",
                    }
                },
                "required": ["city"],
            },
        },
    }
]

# ==========================================================
# Tool registry used by OUR Python program
# ==========================================================
tool_registry = {"get_current_temperature": get_current_temperature}
