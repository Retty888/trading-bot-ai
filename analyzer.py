import openai
from config import OPENAI_API_KEY, GPT4O_MODEL

openai.api_key = OPENAI_API_KEY

def prepare_prompt(candles_dict, news_list, aggressive=False, signal_mode=False):
    lines = []

    if signal_mode:
        lines.append("📊 Signal Request Mode: Generate entry signals across multiple risk profiles.")
    elif aggressive:
        lines.append("⚠️ Aggressive Signal Request: Focus on high-risk/high-reward entries.")
    else:
        lines.append("🧠 Standard Market Analysis:")

    for interval, candles in candles_dict.items():
        lines.append(f"\n--- {interval} candles ---")
        for c in candles:
            if isinstance(c, dict):
                lines.append(
                    f"Time: {c['time']}, Open: {c['open']}, High: {c['high']}, Low: {c['low']}, Close: {c['close']}, Volume: {c['volume']}"
                )
            else:
                lines.append(f"Invalid candle format: {c}")

    lines.append("\n--- News ---")
    for n in news_list:
        if isinstance(n, dict):
            lines.append(f"{n['published_at']} - {n['title']}")
        else:
            lines.append(f"Invalid news format: {n}")

    return "\n".join(lines)

def analyze_market(candles_dict, news_list, model=GPT4O_MODEL, aggressive=False, signal_mode=False):
    prompt = prepare_prompt(candles_dict, news_list, aggressive=aggressive, signal_mode=signal_mode)
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error during analysis: {str(e)}"
