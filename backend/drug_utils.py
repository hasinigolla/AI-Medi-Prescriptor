import random

# Dummy RXCUI mapping (optional placeholder for future use)
def get_rxcui(drug):
    return f"RXCUI_{drug.lower().replace(' ', '_')}"

# Interaction warnings
def get_interactions(drug_list):
    warnings = []
    # Sample interaction logic
    if "ibuprofen" in drug_list and "aspirin" in drug_list:
        warnings.append("⚠ Ibuprofen and Aspirin should not be taken together due to bleeding risk.")
    if "paracetamol" in drug_list and "alcohol" in drug_list:
        warnings.append("⚠ Paracetamol and alcohol can be harmful to the liver.")
    if "metformin" in drug_list and "alcohol" in drug_list:
        warnings.append("⚠ Metformin and alcohol together can cause lactic acidosis.")
    return warnings

# Dosage recommendations based on age
def get_dosage(drugs, age):
    dosage = {}
    for drug in drugs:
        if "unrecognized" in drug:
            dosage[drug] = "❌ Not Available"
        elif age < 12:
            dosage[drug] = "💊 Take half of adult dosage."
        elif age >= 60:
            dosage[drug] = "💊 Use with caution, consult a doctor."
        else:
            dosage[drug] = "💊 1 tablet every 8 hours after meals."
    return dosage

# Suggest alternatives
def suggest_alternatives(drugs):
    alternatives = {}
    alt_dict = {
        "paracetamol": ["acetaminophen", "crocin"],
        "ibuprofen": ["naproxen", "ketoprofen"],
        "aspirin": ["clopidogrel", "acetaminophen"],
        "metformin": ["glipizide", "glyburide"],
        "omeprazole": ["pantoprazole", "ranitidine"]
    }

    for drug in drugs:
        clean_drug = drug.replace(" (unrecognized)", "")
        alternatives[drug] = alt_dict.get(clean_drug, ["No alternatives found"])
    return alternatives