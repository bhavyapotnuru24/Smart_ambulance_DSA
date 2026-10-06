from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Hospital
from app.schemas import HospitalResponse, HospitalCreate, HospitalUpdateBeds

router = APIRouter(prefix="/api/hospitals", tags=["hospitals"])

@router.get("", response_model=List[HospitalResponse])
def get_hospitals(db: Session = Depends(get_db)):
    return db.query(Hospital).all()

@router.put("/{hospital_id}/beds", response_model=HospitalResponse)
def update_hospital_beds(hospital_id: int, payload: HospitalUpdateBeds, db: Session = Depends(get_db)):
    hospital = db.query(Hospital).filter(Hospital.id == hospital_id).first()
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")
    
    hospital.available_beds = max(0, payload.available_beds)
    db.commit()
    db.refresh(hospital)
    return hospital

@router.post("", response_model=HospitalResponse)
def create_hospital(payload: HospitalCreate, db: Session = Depends(get_db)):
    hospital = Hospital(**payload.dict())
    db.add(hospital)
    db.commit()
    db.refresh(hospital)
    return hospital
