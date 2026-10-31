def get_weather(city: str) -> str:
    """Return the sample weather for a supported city.

    The agent may vary capitalization or use common spellings, so normalize
    the input before looking it up.  Raising an error for an unknown city is
    more useful than silently returning ``None`` to the model.
    """
    normalized_city = " ".join(city.strip().casefold().split())
    weather_by_city = {
        "delhi": "sunny",
        "kolkata": "sunny",
        "mumbai": "rainy",
        "hyderabad": "cloudy",
        "hydrabad": "cloudy",
        "bangalore": "rainy",
        "banglor": "rainy",
    }

    try:
        return weather_by_city[normalized_city]
    except KeyError as exc:
        supported = ", ".join(sorted(weather_by_city))
        raise ValueError(
            f"Weather is unavailable for {city!r}. Supported cities: {supported}."
        ) from exc
