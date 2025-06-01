import pandas as pd

def analyze_feature_success(file_path):
    df = pd.read_csv(file_path)

    required_cols = {'entry', 'take_profit', 'direction', 'reasons'}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"CSV должен содержать колонки: {required_cols}")

    # 💡 Учитываем направление сделки
    df['result'] = df.apply(
        lambda row: row['take_profit'] - row['entry'] if row['direction'].lower() == 'long'
        else row['entry'] - row['take_profit'],
        axis=1
    )
    df['successful'] = df['result'] > 0

    # 📋 Ключевые индикаторы/причины
    features = ['EMA', 'MACD', 'RSI', 'ADX', 'VWAP', 'OBV', 'Supertrend', 'Паттерн', 'объёмной зоны']

    ranking = {}
    for feat in features:
        matching = df[df['reasons'].astype(str).str.contains(feat, na=False)]
        success_rate = matching['successful'].mean() if not matching.empty else 0.0
        ranking[feat] = round(success_rate, 3)

    return dict(sorted(ranking.items(), key=lambda x: x[1], reverse=True))
