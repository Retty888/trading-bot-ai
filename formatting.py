
def format_signals_vertical(signals):
    formatted = []
    for signal in signals:
        entry = (
            f"📈 <b>{signal['symbol']}</b>\n"
            f"Направление: {signal['direction']}\n"
            f"Точка входа: {signal['entry']}\n"
            f"Stop Loss: {signal['stop_loss']}\n"
            f"Take Profit: {signal['take_profit']}\n"
            f"Риск: {signal.get('risk', 'n/a')}\n"
            f"Оценка: {signal['confidence']}\n"
        )
        if 'score' in signal:
            entry += f"Score: {signal['score']}/7\n"
        if 'reason' in signal:
            entry += f"Причина: {signal['reason']}\n"
        formatted.append(entry)
    return "\n\n".join(formatted)
