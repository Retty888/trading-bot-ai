# utils/signal_ranker.py

def rank_signal(signal: dict) -> float:
    """
    Возвращает итоговую оценку качества сигнала.
    Оценивается по весам: confidence, score, trend_strength, confirmation_count и отложенность.
    """

    # Значения по умолчанию, если чего-то нет
    confidence_score = {
        "very high": 1.0,
        "high": 0.8,
        "medium": 0.5,
        "low": 0.2,
    }

    # Получаем значения
    confidence = signal.get("confidence", "medium").lower()
    score = float(signal.get("score", 5.0))
    trend_strength = float(signal.get("trend_strength", 0.0))
    confirmation_count = int(signal.get("confirmation_count", 0))
    is_pending = signal.get("is_pending", False)

    # Весовые коэффициенты
    weights = {
        "confidence": 0.35,
        "score": 0.25,
        "trend_strength": 0.2,
        "confirmations": 0.15,
        "penalty_if_pending": -0.2,  # понижаем, если сигнал отложенный
    }

    # Расчёт
    confidence_val = confidence_score.get(confidence, 0.5)
    base_quality = (
        weights["confidence"] * confidence_val +
        weights["score"] * (score / 10.0) +
        weights["trend_strength"] * (trend_strength / 100.0) +
        weights["confirmations"] * min(confirmation_count / 5.0, 1.0)
    )

    # Уменьшаем балл, если это отложенный сигнал
    if is_pending:
        base_quality += weights["penalty_if_pending"]

    # Ограничиваем от 0 до 1
    final_score = max(0.0, min(1.0, base_quality))
    return round(final_score, 4)


def rank_signals(signals: list) -> list:
    """
    Сортирует список сигналов по убыванию их качества (используя rank_signal).
    """
    return sorted(signals, key=rank_signal, reverse=True)
