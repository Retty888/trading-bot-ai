import requests
from datetime import datetime, timedelta
from config import CRYPTOPANIC_API_TOKEN

_last_news_fetch = None
_cached_news = []

def fetch_crypto_news():
    global _last_news_fetch, _cached_news
    now = datetime.utcnow()
    if _last_news_fetch and (now - _last_news_fetch) < timedelta(hours=12):
        return _cached_news

    try:
        url = f"https://cryptopanic.com/api/v1/posts/?auth_token={CRYPTOPANIC_API_TOKEN}&currencies=ETH&public=true&kind=news"
        response = requests.get(url)
        response.raise_for_status()
        news_data = response.json()
        _cached_news = news_data.get("results", [])
        _last_news_fetch = now
        return _cached_news
    except Exception as e:
        print(f"❌ News fetch error: {e}")
        return []