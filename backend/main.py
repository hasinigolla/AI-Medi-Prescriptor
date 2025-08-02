import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
import time
from datetime import datetime

import nlp_utils
from drug_utils import get_rxcui, get_interactions

# Load known drug names (used in fuzzy matching)
with open("drug_list.json") as f:
    known_drugs = json.load(f)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize FastAPI
app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input model
class PrescriptionInput(BaseModel):
    age: int
    prescription: str
    symptoms: str

# 💥 Core API Endpoint
@app.post("/analyze")
async def analyze(data: PrescriptionInput):
    start = time.time()
    print(f"\n[🔵 START] {datetime.now()} - Received Request")

    # STEP 1: Drug Extraction
    t1 = time.time()
    extracted_drugs = nlp_utils.extract_drugs(data.prescription)
    print(f"[1️⃣ Drugs Extracted] Took {round(time.time() - t1, 2)}s")

    # STEP 2: Drug Interactions
    t2 = time.time()
    warnings = []
    for drug in extracted_drugs:
        if "(unrecognized)" in drug:
            continue
        rxcui = get_rxcui(drug)
        if rxcui:
            warnings += get_interactions(rxcui)
    print(f"[2️⃣ Interactions Checked] Took {round(time.time() - t2, 2)}s")

    # STEP 3: Dosage
    t3 = time.time()
    dosage = nlp_utils.suggest_dosage(extracted_drugs, data.age)
    print(f"[3️⃣ Dosage Suggested] Took {round(time.time() - t3, 2)}s")

    # STEP 4: Alternatives
    t4 = time.time()
    suggestions = nlp_utils.suggest_alternatives(extracted_drugs)
    print(f"[4️⃣ Alternatives Suggested] Took {round(time.time() - t4, 2)}s")

    print(f"[✅ END] Total Time: {round(time.time() - start, 2)}s\n")

    return {
        "extracted_drugs": extracted_drugs,
        "interaction_warnings": warnings,
        "safe_dosage": dosage,
        "alternative_suggestions": suggestions
    }