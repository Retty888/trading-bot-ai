
import pandas as pd
import os

SIGNAL_LOG_DIR = "data/signal_logs"

def load_signal_logs():
    all_signals = []
    for file in os.listdir(SIGNAL_LOG_DIR):
        if file.endswith(".csv"):
            df = pd.read_csv(os.path.join(SIGNAL_LOG_DIR, file))
            all_signals.append(df)
    if not all_signals:
        return pd.DataFrame()
    return pd.concat(all_signals, ignore_index=True)

def analyze_performance(df):
    if df.empty:
        return "Нет данных для анализа."

    df['profit'] = df.apply(lambda row: row['take_profit'] - row['entry'] if row['direction'] == 'Long' else row['entry'] - row['take_profit'], axis=1)
    df['success'] = df['profit'] > abs(df['entry'] - df['stop_loss'])
    win_rate = df['success'].mean()
    avg_profit = df['profit'].mean()
    return f"📊 Статистика по {len(df)} сигналам:\nWin rate: {win_rate:.2%}\nСредняя прибыль: {avg_profit:.2f}"

def main():
    logs = load_signal_logs()
    summary = analyze_performance(logs)
    print(summary)

if __name__ == "__main__":
    main()
