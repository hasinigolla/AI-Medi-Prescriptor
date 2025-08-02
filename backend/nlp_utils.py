# nlp_utils.py

from rapidfuzz import process
import json
import os

# Load drug list (you can expand this JSON)
with open("drug_list.json", "r") as f:
    drug_data = json.load(f)

known_drugs = drug_data

def extract_drugs(text):
    words = text.lower().replace(",", " ").replace(".", " ").split()
    extracted = set()

    for word in words:
        match, score, _ = process.extractOne(word, known_drugs)
        if score >= 80:
            extracted.add(match)

    return list(extracted)

def check_interactions(drugs):
    interactions = []
    for i in range(len(drugs)):
        for j in range(i + 1, len(drugs)):
            d1 = drugs[i]
            d2 = drugs[j]
            # Check interaction both ways
            if d2 in drug_data.get(d1, {}).get("interactions", []):
                interactions.append((d1, d2))
            elif d1 in drug_data.get(d2, {}).get("interactions", []):
                interactions.append((d2, d1))
    return interactions

def suggest_dosage(drugs, age):
    dosage = {}
    drug_data = {
        "paracetamol": {"adult": "500mg every 6 hours", "child": "250mg every 6 hours"},
        "ibuprofen": {"adult": "400mg every 8 hours", "child": "200mg every 8 hours"},
        "aspirin": {"adult": "300mg once daily", "child": "Not recommended"},
        # Add more drugs here
    }
    
    for drug in drugs:
        clean_drug = drug.replace(" (unrecognized)", "")
        info = drug_data.get(clean_drug.lower(), {})
        
        if not info:
            dosage[drug] = "N/A"
        else:
            dosage[drug] = info["child"] if age < 12 else info["adult"]
    
    return dosage

# nlp_utils.py

def suggest_alternatives(drugs):
    alternative_data = {
        "paracetamol": ["acetaminophen", "crocin"],
        "ibuprofen": ["naproxen", "diclofenac"],
        "aspirin": ["clopidogrel", "dipyridamole"],
        # Add more mappings
    }

    alternatives = {}
    for drug in drugs:
        clean_drug = drug.replace(" (unrecognized)", "").lower()
        suggestions = alternative_data.get(clean_drug, [])
        alternatives[drug] = suggestions if suggestions else ["No known alternatives"]
    
    return alternatives