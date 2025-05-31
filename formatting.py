def format_signals_vertical(signals, strategy_name="Анализ"):
    formatted = [f"<b>{strategy_name} сигналы:</b>\n"]
    for signal in signals:
        entry = (
            f"📈 <b>{signal['symbol']}</b> — <i>{signal.get('timeframe', '?')}</i>\n"
            f"🔹 Направление: <b>{signal['direction']}</b>\n"
            f"📍 Вход: <code>{signal['entry']}</code>\n"
            f"⛔ SL: <code>{signal['stop_loss']}</code>\n"
            f"🎯 TP: <code>{signal['take_profit']}</code>\n"
            f"🧠 Уверенность: {signal['confidence']} | 🧮 Оценка: {signal.get('score', '?')}/10\n"
        )

        # Обработка блока причин (сжатый формат)
        if 'reasons' in signal and isinstance(signal['reasons'], list):
            # Преобразуем список причин в символы по ключевым словам
            indicator_symbols = []
            for reason in signal['reasons']:
                reason = reason.lower()
                if "rsi" in reason:
                    indicator_symbols.append("📈")
                elif "macd" in reason:
                    indicator_symbols.append("🔁")
                elif "stochastic" in reason:
                    indicator_symbols.append("📊")
                elif "adx" in reason:
                    indicator_symbols.append("📉")
                elif "объём" in reason or "volume" in reason:
                    indicator_symbols.append("📦")
                else:
                    indicator_symbols.append("✅")  # универсальный символ
            entry += f"📋 Индикаторы: {''.join(indicator_symbols)}\n"

        # Добавим AI-анализ, если он есть
        if 'ai_comment' in signal:
            comment_lines = signal['ai_comment'].strip().split("\n")[:4]  # максимум 4 строки
            entry += "🤖 AI-анализ:\n" + "\n".join(comment_lines) + "\n"

        formatted.append(entry)
    return "\n\n".join(formatted)
