# Перевод кода погоды Open-Meteo (WMO id) в читаемый CODE (описание).
# Документация: https://open-meteo.com/en/docs

WEATHER_CODE = {
    0: "clear",
    1: "mainly_clear",
    2: "partly_cloudy",
    3: "overcast",
    45: "foggy",
    48: "rime_fog",
    51: "drizzle_slight",
    53: "drizzle_moderate",
    55: "drizzle_dense",
    56: "freezing_drizzle_slight",
    57: "freezing_drizzle_dense",
    61: "rain_slight",
    63: "rain_moderate",
    65: "rain_heavy",
    66: "freezing_rain_slight",
    67: "freezing_rain_heavy",
    71: "snow_slight",
    73: "snow_moderate",
    75: "snow_heavy",
    77: "snow_grains",
    80: "rain_showers_slight",
    81: "rain_showers_moderate",
    82: "rain_showers_violent",
    85: "snow_showers_slight",
    86: "snow_showers_heavy",
    95: "thunderstorm",
    96: "thunderstorm_slight_hail",
    99: "thunderstorm_heavy_hail",
}


def weather_code_to_str(code: int) -> str:
    """Возвращает CODE (строку) по числовому id погоды Open-Meteo."""
    return WEATHER_CODE.get(code, "unknown")
