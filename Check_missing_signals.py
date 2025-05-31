import pandas as pd

log_file = "logs/signal_log.csv"
df = pd.read_csv(log_file)

missing = df[~df['status'].isin(['TP', 'SL', 'Active'])]
missing.to_csv("logs/unprocessed_signals.csv", index=False)

print(f"❓ Необработанных сигналов: {len(missing)}")
print("✅ Сохранено в logs/unprocessed_signals.csv")

print(missing[['symbol', 'direction', 'entry', 'stop_loss', 'take_profit', 'status']].head(5))
