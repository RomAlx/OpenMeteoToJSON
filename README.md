# OpenMeteoToJSON

Скачивает исторический прогноз погоды из [Open-Meteo Historical Forecast API](https://open-meteo.com/en/docs/historical-forecast-api) и сохраняет в `output/weather.json`.

**Запуск:** `python main.py` — вводишь дату начала (ГГГГ-ММ-ДД), конец всегда «вчера».

**Зависимости:** `pip install -r requirements.txt`

**Конфиг:** координаты и таймзона в `configs/request.py`. Реальные данные API — примерно с 2021-03-22.
