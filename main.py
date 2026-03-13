"""
Скрипт получает исторический дневной прогноз погоды из Open-Meteo (Historical Forecast API),
сохраняет JSON в output/weather.json — массив объектов с полями: date, temperature_min,
temperature_max, humidity, weather_code. Дата начала запрашивается при запуске (в прошлом),
дата окончания — всегда вчера.
"""

import json
import math
from datetime import date, datetime, timedelta, timezone
from typing import cast
from zoneinfo import ZoneInfo

import openmeteo_requests

from configs.request import (
    DAILY_VARS,
    EARLIEST_AVAILABLE_DATE,
    HISTORICAL_FORECAST_URL,
    LATITUDE,
    LONGITUDE,
    OUTPUT_PATH,
    TIMEZONE,
)
from configs.weather_code import weather_code_to_str


def ask_start_date() -> date | None:
    """Запрашивает дату начала (всегда в прошлом)."""
    yesterday = date.today() - timedelta(days=1)
    earliest = cast(date, EARLIEST_AVAILABLE_DATE)
    while True:
        raw = input(
            f"Дата с которой запрашиваем (ГГГГ-ММ-ДД, не позже {yesterday}, "
            f"реальные данные с {earliest}): "
        ).strip()
        if not raw:
            continue
        try:
            parsed = date.fromisoformat(raw)
        except ValueError:
            print("Неверный формат. Введите дату ГГГГ-ММ-ДД.")
            continue
        if parsed > yesterday:
            print("Дата должна быть в прошлом (не позже вчерашнего дня).")
            continue
        if parsed < earliest:
            print(
                f"Внимание: API отдаёт реальные данные только с {earliest}. "
                f"За более ранние даты поля будут null."
            )
        return parsed


def _as_float(v: float | list[float]) -> float:
    """Приводит значение API (float или list[float]) к одному float."""
    return v[0] if isinstance(v, list) else v


def fetch_weather_json(start: date, end: date) -> list[dict]:
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "daily": DAILY_VARS,
        "timezone": TIMEZONE,
    }

    client = openmeteo_requests.Client()
    responses = client.weather_api(HISTORICAL_FORECAST_URL, params=params)
    response = responses[0]
    daily = response.Daily()

    time_start = daily.Time()
    time_interval = daily.Interval()

    def safe_float(val: float):
        return round(val, 1) if not math.isnan(val) else None

    def safe_int(val: float):
        return int(val) if not math.isnan(val) else None

    # Порядок: 0=weather_code, 1=temperature_2m_max, 2=temperature_2m_min, 3=relative_humidity_2m_mean
    n = daily.Variables(0).ValuesLength()
    result = []
    for i in range(n):
        day_start = time_start + i * time_interval
        date_str = datetime.fromtimestamp(day_start, tz=ZoneInfo(TIMEZONE)).strftime("%Y-%m-%d")
        wc_val = _as_float(daily.Variables(0).Values(i))
        result.append({
            "date": date_str,
            "temperature_min": safe_float(_as_float(daily.Variables(2).Values(i))),
            "temperature_max": safe_float(_as_float(daily.Variables(1).Values(i))),
            "humidity": safe_int(_as_float(daily.Variables(3).Values(i))),
            "weather_code": weather_code_to_str(int(wc_val) if not math.isnan(wc_val) else 0),
        })
    return result


if __name__ == "__main__":
    start_date = ask_start_date()
    end_date = date.today() - timedelta(days=1)  # вчера
    data = fetch_weather_json(start_date, end_date)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Сохранено {len(data)} записей в {OUTPUT_PATH}")
