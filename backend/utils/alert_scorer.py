"""Utility to compute a composite severity score for raw alert signals."""


DOMAIN_BASE = {
    "water":     4.0,
    "transit":   3.5,
    "health":    5.0,
    "emergency": 6.0,
}


def score_alert(domain: str, complaint_count: int, anomaly_indicators: int = 0) -> float:
    """
    Returns a severity score 0.0–10.0.
    - base: domain baseline
    - volume bonus: +0.3 per complaint above 5
    - anomaly bonus: +1.0 per confirmed anomaly indicator
    """
    base = DOMAIN_BASE.get(domain, 3.0)
    volume_bonus = max(0, complaint_count - 5) * 0.3
    anomaly_bonus = anomaly_indicators * 1.0
    return min(10.0, round(base + volume_bonus + anomaly_bonus, 2))
