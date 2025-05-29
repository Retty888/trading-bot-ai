
import os
from dotenv import load_dotenv

load_dotenv()

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
print("DEBUG TELEGRAM_BOT_TOKEN:", repr(TELEGRAM_BOT_TOKEN))
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")


# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GPT35_MODEL = "gpt-3.5-turbo"
GPT4_MODEL = "gpt-4"
GPT4O_MODEL = "gpt-4o"
USE_GPT35 = True
USE_GPT4 = True
USE_GPT4O = True

# CryptoPanic
CRYPTOPANIC_API_TOKEN = os.getenv("CRYPTOPANIC_API_TOKEN")

# Bot mode
ANALYSIS_MODE = os.getenv("ANALYSIS_MODE", "neutral")

# Binance
BINANCE_API_BASE = "https://api.binance.com"
PAIR = "ETHUSDT"
BINANCE_API_KEY = None
BINANCE_API_SECRET = None


INTERVALS = {
    "1m": "1m",
    "5m": "5m",
    "1h": "1h",
    "4h": "4h"
}
LIMITS = {
    "1m": 1500,
    "5m": 1440,
    "1h": 300,
    "4h": 150
}

# Language
LANGUAGE = os.getenv("LANGUAGE", "en")
