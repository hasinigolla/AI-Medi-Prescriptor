# backend/model.py

from transformers import pipeline

# Load zero-shot classification model
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Sample drug categories and interactions
drug_categories = {
    "Paracetamol": ["Pain reliever", "Fever reducer"],
    "Ibuprofen": ["Anti-inflammatory", "Pain reliever"],
    "Amoxicillin": ["Antibiotic"],
    "Cetirizine": ["Antihistamine"],
    "Atorvastatin": ["Cholesterol reducer"],
    "Metformin": ["Diabetes medication"],
}

dangerous_pairs = [
    ("Ibuprofen", "Aspirin"),
    ("Amoxicillin", "Methotrexate"),
    ("Cetirizine", "Alcohol"),
]

# Analyze the prescription
def analyze_prescription(drugs: list, age: int):
    interactions = []
    suggestions = []

    # Check for harmful combinations
    for i in range(len(drugs)):
        for j in range(i + 1, len(drugs)):
            if (drugs[i], drugs[j]) in dangerous_pairs or (drugs[j], drugs[i]) in dangerous_pairs:
                interactions.append(f"⚠️ {drugs[i]} and {drugs[j]} may interact harmfully.")

    # Recommend based on age (example rule)
    if age < 12:
        for drug in drugs:
            if drug in ["Ibuprofen"]:
                suggestions.append(f"❗ {drug} is not recommended for children under 12.")

    # Use zero-shot classification to predict purpose
    purposes = []
    for drug in drugs:
        categories = drug_categories.get(drug, [])
        if categories:
            purpose = ", ".join(categories)
        else:
            prediction = classifier(drug, candidate_labels=["Pain reliever", "Antibiotic", "Antihistamine", "Diabetes medication"])
            purpose = prediction['labels'][0]
        purposes.append(f"{drug} is used for: {purpose}")

    return {
        "interactions": interactions or ["✅ No major interactions detected."],
        "suggestions": suggestions or ["✅ No age-based suggestions."],
        "purposes": purposes
    }
