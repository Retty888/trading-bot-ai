# config.py

# Telegram settings
TELEGRAM_BOT_TOKEN = "7543302550:AAHJWuhGuD3a3-Z_fgeWeN-iUILNz5mwdX0"
TELEGRAM_CHAT_ID = "230671821"  # Либо -4947537406 если в группе

# OpenAI settings
OPENAI_API_KEY = "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"
GPT35_MODEL = "gpt-3.5-turbo"
GPT4_MODEL = "gpt-4"
GPT4O_MODEL = "gpt-4o"
USE_GPT35 = True
USE_GPT4 = True
USE_GPT4O = True

# CryptoPanic API
CRYPTOPANIC_API_TOKEN = "5caa3e23544d47c86a5cbe432ef3bad1c6876d41"

# Bot mode
ANALYSIS_MODE = "neutral"  # active, neutral, off

# Binance API config
BINANCE_API_BASE = "https://api.binance.com"
PAIR = "ETHUSDT"
INTERVALS = {
    "5m": "5m",
    "1h": "1h",
    "4h": "4h"
}
LIMITS = {
    "5m": 1440,
    "1h": 300,
    "4h": 150
}

# Language setting: "en" or "ru"
LANGUAGE = "ru"
