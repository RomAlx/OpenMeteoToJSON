"""
Параметры запроса к Open-Meteo Historical Forecast API и ограничения по датам.

Ограничения API:
- Historical Forecast API отдаёт архив сохранённых прогнозов; реальные данные
  (температура, влажность и т.д.) доступны примерно с EARLIEST_AVAILABLE_DATE.
  Запросы на более ранние даты возвращают строки с null в полях.
- Дата окончания — не позже вчерашнего дня (прогнозы архивируются с задержкой).
"""

from datetime import date
from pathlib import Path

# — Координаты и таймзона —
LATITUDE = 55.7558
LONGITUDE = 37.6173
TIMEZONE = "Europe/Moscow"

# — Путь к выходному файлу —
OUTPUT_PATH = Path("output/weather.json")

# — API —
HISTORICAL_FORECAST_URL = "https://historical-forecast-api.open-meteo.com/v1/forecast"
DAILY_VARS = [
    "weather_code",
    "temperature_2m_max",
    "temperature_2m_min",
    "relative_humidity_2m_mean",
]

# — Ограничения по датам —
# Самая ранняя дата, с которой API возвращает осмысленные данные (не null).
# Ранее этой даты архив прогнозов недоступен или не заполнен.
EARLIEST_AVAILABLE_DATE = date(2021, 3, 22)
