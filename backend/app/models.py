from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class AdminUser(Base):
    __tablename__ = "admin_users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

class Hospital(Base):
    __tablename__ = "hospitals"

    id = Column(Integer, primary_key=True, index=True)
    hospital_name = Column(String(100), nullable=False)
    address = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    specializations = Column(Text, nullable=False)  # Comma-separated list e.g. "Cardiology,Neurology,Emergency"
    total_beds = Column(Integer, nullable=False, default=50)
    available_beds = Column(Integer, nullable=False, default=10)
    phone = Column(String(20), nullable=True)

    doctors = relationship("Doctor", back_populates="hospital")
    dispatches = relationship("Dispatch", back_populates="hospital")

class Ambulance(Base):
    __tablename__ = "ambulances"

    id = Column(Integer, primary_key=True, index=True)
    ambulance_code = Column(String(20), unique=True, index=True, nullable=False)  # A01, A02, etc.
    status = Column(String(20), nullable=False, default="Available")  # Available, Busy, Dispatched
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    driver_name = Column(String(100), nullable=True)
    driver_phone = Column(String(20), nullable=True)

    dispatches = relationship("Dispatch", back_populates="ambulance")

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    specialization = Column(String(100), nullable=False)
    is_available = Column(Boolean, default=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=False)

    hospital = relationship("Hospital", back_populates="doctors")
    dispatches = relationship("Dispatch", back_populates="doctor")

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    phone = Column(String(20), nullable=True)
    medical_history = Column(Text, nullable=True)

class Emergency(Base):
    __tablename__ = "emergencies"

    id = Column(Integer, primary_key=True, index=True)
    emergency_code = Column(String(50), unique=True, index=True, nullable=False)
    patient_name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    emergency_type = Column(String(100), nullable=False)  # Chest Pain, Breathing Problem, Accident / Injury, Other
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    priority = Column(String(20), default="Normal")  # High, Normal
    status = Column(String(30), default="Pending")  # Pending, Dispatched, Completed, Cancelled
    created_at = Column(DateTime, default=datetime.utcnow)

    dispatch = relationship("Dispatch", back_populates="emergency", uselist=False)

class Dispatch(Base):
    __tablename__ = "dispatches"

    id = Column(Integer, primary_key=True, index=True)
    emergency_id = Column(Integer, ForeignKey("emergencies.id"), nullable=False)
    ambulance_id = Column(Integer, ForeignKey("ambulances.id"), nullable=False)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=True)
    route_info = Column(Text, nullable=True)  # JSON or descriptive text of chosen route
    eta_minutes = Column(Integer, nullable=True)
    status = Column(String(30), default="Active")  # Active, Completed
    dispatched_at = Column(DateTime, default=datetime.utcnow)

    emergency = relationship("Emergency", back_populates="dispatch")
    ambulance = relationship("Ambulance", back_populates="dispatches")
    hospital = relationship("Hospital", back_populates="dispatches")
    doctor = relationship("Doctor", back_populates="dispatches")
