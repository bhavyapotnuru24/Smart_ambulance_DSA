from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

# Admin Auth Schemas
class AdminLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str

# Hospital Schemas
class HospitalBase(BaseModel):
    hospital_name: str
    address: str
    latitude: float
    longitude: float
    specializations: str
    total_beds: int
    available_beds: int
    phone: Optional[str] = None

class HospitalCreate(HospitalBase):
    pass

class HospitalUpdateBeds(BaseModel):
    available_beds: int

class HospitalResponse(HospitalBase):
    id: int
    class Config:
        from_attributes = True

# Doctor Schemas
class DoctorBase(BaseModel):
    name: str
    specialization: str
    is_available: bool = True
    hospital_id: int

class DoctorCreate(DoctorBase):
    pass

class DoctorResponse(DoctorBase):
    id: int
    hospital_name: Optional[str] = None
    class Config:
        from_attributes = True

# Ambulance Schemas
class AmbulanceBase(BaseModel):
    ambulance_code: str
    status: str
    latitude: float
    longitude: float
    driver_name: Optional[str] = None
    driver_phone: Optional[str] = None

class AmbulanceStatusUpdate(BaseModel):
    status: str

class AmbulanceResponse(AmbulanceBase):
    id: int
    class Config:
        from_attributes = True

# Patient Schemas
class PatientBase(BaseModel):
    patient_id: str
    name: str
    age: int
    phone: Optional[str] = None
    medical_history: Optional[str] = None

class PatientResponse(PatientBase):
    id: int
    class Config:
        from_attributes = True

# Emergency Request Schema (No severity field as requested!)
class EmergencyCreate(BaseModel):
    patient_name: str
    age: int
    emergency_type: str  # Chest Pain, Breathing Problem, Accident / Injury, Other
    latitude: float
    longitude: float
    phone: Optional[str] = "9999999999"

class EmergencyResponse(BaseModel):
    id: int
    emergency_code: str
    patient_name: str
    age: int
    emergency_type: str
    latitude: float
    longitude: float
    priority: str
    status: str
    created_at: datetime
    class Config:
        from_attributes = True

# Route Information Schema
class RouteOption(BaseModel):
    id: int
    name: str
    distance_km: float
    eta_minutes: int
    is_recommended: bool
    path: List[List[float]]  # List of [lat, lng] coordinates
    traffic_level: str

# Dispatch Response Schema
class DispatchResultResponse(BaseModel):
    dispatch_id: int
    emergency_code: str
    emergency_status: str
    priority: str
    ambulance: AmbulanceResponse
    hospital: HospitalResponse
    assigned_doctor: Optional[DoctorResponse] = None
    existing_patient_record: Optional[PatientResponse] = None
    match_method: Optional[str] = None  # Exact (KMP) or Fuzzy (Edit Distance) or New
    selected_route: RouteOption
    alternative_routes: List[RouteOption]
    dsa_explanation: Dict[str, Any]

# Admin Dashboard Stats
class DashboardStatsResponse(BaseModel):
    total_hospitals: int
    hospitals_with_available_beds: int
    hospitals_zero_beds: int
    total_ambulances: int
    available_ambulances: int
    busy_ambulances: int
    dispatched_ambulances: int
    total_doctors: int
    available_doctors: int
    active_emergencies: int
