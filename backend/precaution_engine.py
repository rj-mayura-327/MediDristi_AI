from typing import List


def generate_precaution_plan(parameter_results: List[dict]) -> dict:
    daily = [
        "Exercise 30 minutes daily",
        "Drink at least 2-3 liters of water",
        "Get 7-8 hours of sleep",
    ]
    lifestyle = [
        "Reduce processed food intake",
        "Choose whole foods over packaged snacks",
        "Maintain a regular meal schedule",
    ]
    monitoring = [
        "Review your medical report values weekly",
        "Track symptoms such as fatigue and thirst",
    ]
    follow_up = [
        "Consult a physician for persistent abnormalities",
        "Share results with your healthcare provider",
    ]

    for item in parameter_results:
        name = item["parameter"].lower()
        status = item["status"]
        if status == "Normal":
            continue
        if "hemoglobin" in name:
            lifestyle.append("Include iron-rich meals and vitamin C with iron sources")
            monitoring.append("Monitor energy and endurance levels regularly")
        if "cholesterol" in name:
            daily.append("Prioritize physical activity like walking or gentle exercise")
            lifestyle.append("Limit high-fat and fried foods")
            follow_up.append("Discuss lipid management with your doctor")
        if "blood sugar" in name or "glucose" in name:
            daily.append("Monitor carbohydrate portions at every meal")
            lifestyle.append("Avoid sugary beverages and snacks")
            follow_up.append("Check blood sugar with a healthcare provider if levels remain high")
        if "vitamin d" in name:
            lifestyle.append("Spend time outdoors for sunlight exposure")
            follow_up.append("Consider a vitamin D test in three months")
        if name in {"creatinine", "urea"}:
            monitoring.append("Watch fluid intake and kidney-related symptoms")
            follow_up.append("Consult for kidney function monitoring")
        if name in {"ast", "alt", "alp", "bilirubin"}:
            lifestyle.append("Avoid alcohol and heavy liver stress")
            follow_up.append("Evaluate liver enzymes with your doctor")

    return {
        "daily_precautions": list(dict.fromkeys(daily)),
        "lifestyle_changes": list(dict.fromkeys(lifestyle)),
        "monitoring_recommendations": list(dict.fromkeys(monitoring)),
        "medical_follow_up": list(dict.fromkeys(follow_up)),
    }
