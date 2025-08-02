import requests
import json
import time

def get_drugs_from_letter(letter):
    url = f"https://rxnav.nlm.nih.gov/REST/drugs.json?name={letter}"
    try:
        response = requests.get(url)
        data = response.json()
        drugs = set()
        for group in data.get("drugGroup", {}).get("conceptGroup", []):
            for concept in group.get("conceptProperties", []):
                name = concept.get("name")
                if name:
                    drugs.add(name)
        return drugs
    except Exception as e:
        print(f"Error fetching for {letter}: {e}")
        return set()

all_drugs = set()
for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    drugs = get_drugs_from_letter(ch)
    all_drugs.update(drugs)
    time.sleep(0.5)  # Avoid hitting API too fast

# Save to file
with open("drug_list.json", "w") as f:
    json.dump(sorted(all_drugs), f, indent=2)

print(f"✅ Saved {len(all_drugs)} drug names to drug_list.json")