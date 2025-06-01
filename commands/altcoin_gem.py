from telegram import Update
from telegram.ext import ContextTypes
import requests
import random

# Команда /altcoin_gem
async def handle_altcoin_gem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Получаем список торговых пар на MEXC
        mexc_response = requests.get("https://api.mexc.com/api/v3/exchangeInfo")
        mexc_data = mexc_response.json()
        mexc_symbols = set()
        for symbol_info in mexc_data.get("symbols", []):
            if symbol_info.get("quoteAsset") == "USDT":
                mexc_symbols.add(symbol_info.get("baseAsset"))

        # Получаем рыночные данные по монетам с CoinGecko
        coingecko_response = requests.get(
            "https://api.coingecko.com/api/v3/coins/markets",
            params={
                "vs_currency": "usd",
                "order": "market_cap_asc",
                "per_page": 250,
                "page": 1,
                "sparkline": False
            }
        )
        coins = coingecko_response.json()

        # Фильтруем монеты по критериям
        candidates = []
        for coin in coins:
            symbol = coin.get("symbol", "").upper()
            market_cap = coin.get("market_cap", 0)
            volume = coin.get("total_volume", 0)
            if (
                market_cap and market_cap < 50_000_000 and
                volume and volume > 500_000 and
                symbol in mexc_symbols
            ):
                candidates.append(coin)

        if not candidates:
            await update.message.reply_text("⚠️ Не удалось найти подходящий альткоин.")
            return

        # Выбираем случайную монету из списка
        selected_coin = random.choice(candidates)
        name = selected_coin.get("name")
        symbol = selected_coin.get("symbol").upper()
        market_cap = selected_coin.get("market_cap")
        volume = selected_coin.get("total_volume")
        price = selected_coin.get("current_price")
        mexc_link = f"https://www.mexc.com/exchange/{symbol}_USDT"

        message = (
            f"💎 Перспективный Altcoin:\n"
            f"Название: {name} ({symbol})\n"
            f"Цена: ${price:,.2f}\n"
            f"Рыночная капитализация: ${market_cap:,.0f}\n"
            f"Объём за 24ч: ${volume:,.0f}\n"
            f"🔗 [Торговая пара на MEXC]({mexc_link})"
        )

        await update.message.reply_text(message, parse_mode="Markdown")

    except Exception as e:
        print(f"[❌] Ошибка в handle_altcoin_gem: {e}")
        await update.message.reply_text("❌ Произошла ошибка при получении данных.")
