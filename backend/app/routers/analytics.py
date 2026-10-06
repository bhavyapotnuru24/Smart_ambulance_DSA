from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Hospital, Ambulance, Doctor, Emergency
from app.schemas import DashboardStatsResponse

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

@router.get("/dashboard", response_model=DashboardStatsResponse)
def get_dashboard_stats(db: Session = Depends(get_db)):
    hospitals = db.query(Hospital).all()
    ambulances = db.query(Ambulance).all()
    doctors = db.query(Doctor).all()
    emergencies = db.query(Emergency).filter(Emergency.status == "Dispatched").all()

    total_hospitals = len(hospitals)
    hospitals_with_beds = len([h for h in hospitals if h.available_beds > 0])
    hospitals_zero_beds = len([h for h in hospitals if h.available_beds == 0])

    total_ambulances = len(ambulances)
    available_ambulances = len([a for a in ambulances if a.status == "Available"])
    busy_ambulances = len([a for a in ambulances if a.status == "Busy"])
    dispatched_ambulances = len([a for a in ambulances if a.status == "Dispatched"])

    total_doctors = len(doctors)
    available_doctors = len([d for d in doctors if d.is_available])

    return DashboardStatsResponse(
        total_hospitals=total_hospitals,
        hospitals_with_available_beds=hospitals_with_beds,
        hospitals_zero_beds=hospitals_zero_beds,
        total_ambulances=total_ambulances,
        available_ambulances=available_ambulances,
        busy_ambulances=busy_ambulances,
        dispatched_ambulances=dispatched_ambulances,
        total_doctors=total_doctors,
        available_doctors=available_doctors,
        active_emergencies=len(emergencies)
    )
