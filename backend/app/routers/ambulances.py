from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Ambulance
from app.schemas import AmbulanceResponse, AmbulanceStatusUpdate

router = APIRouter(prefix="/api/ambulances", tags=["ambulances"])

@router.get("", response_model=List[AmbulanceResponse])
def get_ambulances(db: Session = Depends(get_db)):
    return db.query(Ambulance).order_by(Ambulance.ambulance_code).all()

@router.put("/{ambulance_id}/status", response_model=AmbulanceResponse)
def update_ambulance_status(ambulance_id: int, payload: AmbulanceStatusUpdate, db: Session = Depends(get_db)):
    amb = db.query(Ambulance).filter(Ambulance.id == ambulance_id).first()
    if not amb:
        raise HTTPException(status_code=404, detail="Ambulance not found")
    
    valid_statuses = ["Available", "Busy", "Dispatched"]
    if payload.status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of {valid_statuses}")
    
    amb.status = payload.status
    db.commit()
    db.refresh(amb)
    return amb

@router.post("/{ambulance_id}/reset", response_model=AmbulanceResponse)
def reset_ambulance_status(ambulance_id: int, db: Session = Depends(get_db)):
    amb = db.query(Ambulance).filter(Ambulance.id == ambulance_id).first()
    if not amb:
        raise HTTPException(status_code=404, detail="Ambulance not found")
    
    amb.status = "Available"
    db.commit()
    db.refresh(amb)
    return amb
