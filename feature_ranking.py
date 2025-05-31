import pandas as pd

def analyze_feature_success(file_path):
    df = pd.read_csv(file_path)
    df['result'] = df['take_profit'] - df['entry']
    df['successful'] = df['result'] > 0
    features = ['EMA', 'MACD', 'RSI', 'ADX', 'VWAP', 'OBV', 'Supertrend', 'Паттерн', 'объёмной зоны']

    ranking = {}
    for feat in features:
        matching = df[df['reasons'].str.contains(feat, na=False)]
        success_rate = matching['successful'].mean() if not matching.empty else 0.0
        ranking[feat] = round(success_rate, 2)

    return dict(sorted(ranking.items(), key=lambda x: x[1], reverse=True))
