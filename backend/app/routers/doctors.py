from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Doctor, Hospital
from app.schemas import DoctorResponse, DoctorCreate

router = APIRouter(prefix="/api/doctors", tags=["doctors"])

@router.get("", response_model=List[DoctorResponse])
def get_doctors(db: Session = Depends(get_db)):
    doctors = db.query(Doctor).all()
    results = []
    for doc in doctors:
        d_dict = DoctorResponse.model_validate(doc)
        if doc.hospital:
            d_dict.hospital_name = doc.hospital.hospital_name
        results.append(d_dict)
    return results

@router.put("/{doctor_id}/toggle-availability", response_model=DoctorResponse)
def toggle_doctor_availability(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    doctor.is_available = not doctor.is_available
    db.commit()
    db.refresh(doctor)
    res = DoctorResponse.model_validate(doctor)
    if doctor.hospital:
        res.hospital_name = doctor.hospital.hospital_name
    return res

@router.post("", response_model=DoctorResponse)
def create_doctor(payload: DoctorCreate, db: Session = Depends(get_db)):
    hospital = db.query(Hospital).filter(Hospital.id == payload.hospital_id).first()
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")
    
    doctor = Doctor(**payload.dict())
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    res = DoctorResponse.model_validate(doctor)
    res.hospital_name = hospital.hospital_name
    return res
