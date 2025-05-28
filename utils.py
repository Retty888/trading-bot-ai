import requests
from datetime import datetime, timedelta

def get_openai_usage(api_key):
    try:
        # Определяем даты начала и окончания (последние 30 дней)
        end_date = datetime.utcnow().date()
        start_date = end_date - timedelta(days=30)

        # Форматируем даты в строку
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')

        # Запрос к API OpenAI для получения информации об использовании
        url = f"https://api.openai.com/v1/dashboard/billing/usage?start_date={start_date_str}&end_date={end_date_str}"
        headers = {
            "Authorization": f"Bearer {api_key}"
        }

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return f"❌ Ошибка при получении данных об использовании: {response.status_code} - {response.text}"

        data = response.json()
        total_usage = data.get("total_usage", 0)
        total_usage_dollars = total_usage / 100.0  # Преобразуем из центов в доллары

        return f"📊 Использование OpenAI за последние 30 дней: ${total_usage_dollars:.2f}"

    except Exception as e:
        return f"❌ Ошибка при получении данных об использовании: {str(e)}"
