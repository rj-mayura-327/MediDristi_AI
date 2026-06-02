from typing import List

CONDITION_RECOMMENDATIONS = {
    "low hemoglobin": {
        "include": ["Spinach", "Dates", "Beetroot", "Pomegranate", "Lentils", "Lean red meat"],
        "limit": ["Caffeine with meals", "Refined grains", "High-sugar snacks"],
        "hydration": ["Water throughout the day", "Limit sugary beverages"],
        "nutrition": ["Iron-rich foods", "Vitamin C with meals", "Balanced protein intake"],
    },
    "high cholesterol": {
        "include": ["Oats", "Fruits", "Vegetables", "Fatty fish", "Nuts"],
        "limit": ["Processed foods", "Fried foods", "Saturated fats", "Sugary drinks"],
        "hydration": ["Water and herbal teas", "Avoid sweetened beverages"],
        "nutrition": ["Fiber-rich meals", "Lean proteins", "Healthy fats"],
    },
    "high blood sugar": {
        "include": ["Whole grains", "Leafy greens", "Berries", "Beans", "Water"],
        "limit": ["Refined carbohydrates", "Sugary snacks", "Sweetened beverages"],
        "hydration": ["Regular water intake", "Limit fruit juices"],
        "nutrition": ["Portion control", "Complex carbohydrates", "Consistent meal timing"],
    },
    "low vitamin d": {
        "include": ["Fortified milk", "Egg yolk", "Mushrooms", "Fatty fish", "Sunlight exposure"],
        "limit": ["High-sugar foods", "Highly processed snacks"],
        "hydration": ["Water intake", "Balanced fluids"],
        "nutrition": ["Vitamin D rich foods", "Healthy fats for absorption"],
    },
    "kidney concern": {
        "include": ["Fresh vegetables", "Lean proteins", "Low-sodium foods"],
        "limit": ["High-sodium snacks", "Processed meats", "Excessive dairy"],
        "hydration": ["Steady water intake", "Avoid soda"],
        "nutrition": ["Controlled protein portions", "Low-sodium cooking"],
    },
    "liver concern": {
        "include": ["Leafy greens", "Berries", "Whole grains", "Green tea"],
        "limit": ["Alcohol", "Fried foods", "Sugary beverages"],
        "hydration": ["Plenty of water", "Avoid excessive caffeine"],
        "nutrition": ["Antioxidant-rich foods", "Balanced carbohydrates"],
    },
}

DEFAULT_DIET = {
    "include": ["Fruits", "Vegetables", "Whole grains", "Lean proteins"],
    "limit": ["Processed foods", "Excess salt", "Refined sugar"],
    "hydration": ["Drink at least 2-3 liters of water", "Choose water over soda"],
    "nutrition": ["Eat balanced meals", "Focus on fiber and lean protein"],
}


def generate_diet_recommendations(parameter_results: List[dict]) -> dict:
    include = set(DEFAULT_DIET["include"])
    limit = set(DEFAULT_DIET["limit"])
    hydration = set(DEFAULT_DIET["hydration"])
    nutrition = set(DEFAULT_DIET["nutrition"])

    for item in parameter_results:
        name = item["parameter"].lower()
        status = item["status"]
        if status != "Normal":
            if "hemoglobin" in name:
                recommendations = CONDITION_RECOMMENDATIONS["low hemoglobin"]
            elif "cholesterol" in name:
                recommendations = CONDITION_RECOMMENDATIONS["high cholesterol"]
            elif "blood sugar" in name or "glucose" in name:
                recommendations = CONDITION_RECOMMENDATIONS["high blood sugar"]
            elif "vitamin d" in name:
                recommendations = CONDITION_RECOMMENDATIONS["low vitamin d"]
            elif name in {"creatinine", "urea"}:
                recommendations = CONDITION_RECOMMENDATIONS["kidney concern"]
            elif name in {"ast", "alt", "alp", "bilirubin"}:
                recommendations = CONDITION_RECOMMENDATIONS["liver concern"]
            else:
                continue

            include.update(recommendations["include"])
            limit.update(recommendations["limit"])
            hydration.update(recommendations["hydration"])
            nutrition.update(recommendations["nutrition"])

    return {
        "include": sorted(include),
        "limit": sorted(limit),
        "hydration": sorted(hydration),
        "nutrition": sorted(nutrition),
    }
