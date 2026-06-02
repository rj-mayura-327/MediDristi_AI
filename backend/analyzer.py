import re
from typing import Dict, List

from .health_score import calculate_health_score, risk_level

REFERENCE_RANGES = {
    "hemoglobin": {"normal": (12.0, 17.5), "unit": "g/dL"},
    "rbc": {"normal": (3.8, 5.8), "unit": "million/µL"},
    "wbc": {"normal": (4.0, 11.0), "unit": "10^3/µL"},
    "platelets": {"normal": (150, 450), "unit": "10^3/µL"},
    "blood sugar": {"normal": (70, 110), "unit": "mg/dL"},
    "cholesterol": {"normal": (0, 200), "unit": "mg/dL"},
    "vitamin d": {"normal": (30, 100), "unit": "ng/mL"},
    "creatinine": {"normal": (0.6, 1.3), "unit": "mg/dL"},
    "ast": {"normal": (10, 40), "unit": "U/L"},
    "alt": {"normal": (7, 56), "unit": "U/L"},
    "alp": {"normal": (44, 147), "unit": "U/L"},
    "bilirubin": {"normal": (0.1, 1.2), "unit": "mg/dL"},
    "urea": {"normal": (7, 20), "unit": "mg/dL"},
}

EXPLANATIONS = {
    "hemoglobin": {
        "normal": "Hemoglobin is within the normal range, showing your blood is carrying oxygen effectively.",
        "high": "High hemoglobin may signal dehydration, smoking, or certain blood disorders.",
        "low": "Low hemoglobin suggests anemia or reduced oxygen delivery to tissues.",
    },
    "rbc": {
        "normal": "Your red cell count is healthy and supports oxygen delivery.",
        "high": "A high RBC count can be linked to dehydration or stress.",
        "low": "A low RBC count may indicate anemia or nutrient deficiency.",
    },
    "wbc": {
        "normal": "White blood cells appear normal, indicating stable immune response.",
        "high": "High WBC may signal infection or inflammation.",
        "low": "Low WBC can suggest immune suppression or bone marrow stress.",
    },
}


def _parse_number(value: str) -> float:
    if value is None:
        return 0.0
    cleaned = re.sub(r"[^\d\.\-]", "", str(value))
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def _classify_value(name: str, numeric: float) -> str:
    if name not in REFERENCE_RANGES:
        return "Normal"

    low, high = REFERENCE_RANGES[name]["normal"]
    if numeric < low:
        return "Low"
    if numeric > high:
        return "High"
    return "Normal"


def _build_message(name: str, status: str) -> Dict[str, str]:
    explanation = EXPLANATIONS.get(name, {})
    if status == "Normal":
        return {
            "medical_explanation": explanation.get(
                "normal",
                f"{name.title()} is in the expected clinical range."
            ),
            "simple_explanation": (
                f"Your {name.title()} level is normal. This means your body is likely functioning well in this area."
            ),
        }
    if status == "High":
        return {
            "medical_explanation": explanation.get(
                "high",
                f"{name.title()} is above the normal range and may need evaluation."
            ),
            "simple_explanation": (
                f"Your {name.title()} is higher than expected, which may need attention."
            ),
        }
    return {
        "medical_explanation": explanation.get(
            "low",
            f"{name.title()} is below the normal range and may require follow-up."
        ),
        "simple_explanation": (
            f"Your {name.title()} is lower than expected, which may affect your health."
        ),
    }


def analyze_parameters(parsed_values: dict) -> List[dict]:
    results = []
    for name, raw_value in parsed_values.items():
        numeric = _parse_number(raw_value)
        status = _classify_value(name, numeric)
        reference = REFERENCE_RANGES.get(name, {})
        normal_range = (
            f"{reference['normal'][0]} - {reference['normal'][1]} {reference['unit']}"
            if reference else "Not defined"
        )
        messages = _build_message(name, status)

        results.append(
            {
                "parameter": name.title(),
                "value": str(raw_value),
                "normal_range": normal_range,
                "status": status,
                "medical_explanation": messages["medical_explanation"],
                "simple_explanation": messages["simple_explanation"],
            }
        )
    return sorted(results, key=lambda item: item["parameter"])


def generate_health_summary(parameter_results: List[dict]) -> dict:
    score = calculate_health_score(parameter_results)
    level = risk_level(score)
    findings = [f"{item['parameter']}: {item['status']}" for item in parameter_results if item["status"] != "Normal"]
    positives = [item["parameter"] for item in parameter_results if item["status"] == "Normal"]
    concerns = [item["parameter"] for item in parameter_results if item["status"] != "Normal"]

    return {
        "health_score": f"{score}/100",
        "risk_level": level,
        "key_findings": findings or ["No significant abnormalities found."],
        "positive_findings": positives or ["Most parameters are within normal limits."],
        "areas_of_concern": concerns or ["No major concerns detected."],
    }
