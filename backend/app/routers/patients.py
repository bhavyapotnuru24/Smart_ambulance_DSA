from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from app.database import get_db
from app.models import Patient
from app.schemas import PatientResponse
from app.dsa.kmp import kmp_search
from app.dsa.edit_distance import fuzzy_search_patient

router = APIRouter(prefix="/api/patients", tags=["patients"])

@router.get("", response_model=List[PatientResponse])
def get_patients(db: Session = Depends(get_db)):
    return db.query(Patient).all()

@router.get("/search")
def search_patient_records(query: str = Query(..., description="Patient name or ID"), db: Session = Depends(get_db)):
    """
    DSA Concepts F & G Demonstration Endpoint:
    1. First tries exact pattern search using KMP algorithm.
    2. If no exact match is found, falls back to Edit Distance DP fuzzy match.
    """
    all_patients = db.query(Patient).all()
    
    # 1. KMP Exact Substring Search
    kmp_matches = []
    for p in all_patients:
        if kmp_search(p.name, query) or kmp_search(query, p.name) or kmp_search(p.patient_id, query):
            kmp_matches.append(p)
            
    if kmp_matches:
        return {
            "match_found": True,
            "algorithm_used": "KMP String Matching (O(N+M) Exact Match)",
            "patients": [PatientResponse.model_validate(p) for p in kmp_matches]
        }
        
    # 2. Edit Distance Fuzzy Search
    fuzzy_patient, distance = fuzzy_search_patient(all_patients, query, max_distance=3)
    if fuzzy_patient:
        return {
            "match_found": True,
            "algorithm_used": f"Edit Distance Dynamic Programming (Levenshtein Distance = {distance})",
            "patients": [PatientResponse.model_validate(fuzzy_patient)]
        }
        
    return {
        "match_found": False,
        "algorithm_used": "KMP + Edit Distance",
        "patients": []
    }
