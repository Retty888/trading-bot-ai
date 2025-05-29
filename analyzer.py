
import openai
from config import OPENAI_API_KEY, GPT4O_MODEL

openai.api_key = OPENAI_API_KEY

def prepare_prompt(candles_dict, news_list, aggressive=False, signal_mode=False):
    lines = []

    if signal_mode:
        lines.append(
            "📶 Signal Mode Request:\n"
            "Generate only active, high-confidence trading signals across major crypto pairs.\n"
            "For each signal, return the following structured format as a table:\n"
            "| Symbol | Direction | Entry | Stop-Loss | Take-Profit | Risk Level |\n"
            "|--------|-----------|-------|-----------|-------------|------------|\n"
            "Include only assets with clear signals within the current or next 1 hour.\n"
            "Be concise. No explanations. If no strong signals — say so clearly.\n"
        )
    elif aggressive:
        lines.append("⚠️ Aggressive Analysis Mode: focus on risky/high-reward signals.")
    else:
        lines.append("🧠 Standard Market Analysis:")

    for interval, candles in candles_dict.items():
        lines.append(f"\n--- {interval} candles ---")
        for c in candles:
            if isinstance(c, dict):
                lines.append(
                    f"Time: {c['time']}, Open: {c['open']}, High: {c['high']}, Low: {c['low']}, Close: {c['close']}, Volume: {c['volume']}"
                )

    lines.append("\n--- News ---")
    for n in news_list:
        if isinstance(n, dict):
            lines.append(f"{n['published_at']} - {n['title']}")

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
