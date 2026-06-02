from typing import List

RISK_THRESHOLDS = {
    "low": 80,
    "moderate": 60,
    "high": 40,
}


def calculate_health_score(parameter_results: List[dict]) -> int:
    if not parameter_results:
        return 70

    score = 100
    for param in parameter_results:
        status = param.get("status", "Normal")
        if status == "High" or status == "Low":
            score -= 10
        if status == "Borderline":
            score -= 5
    score = max(0, min(100, score))
    return score


def risk_level(score: int) -> str:
    if score >= RISK_THRESHOLDS["low"]:
        return "Low"
    if score >= RISK_THRESHOLDS["moderate"]:
        return "Moderate"
    return "High"
