from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import auth, hospitals, doctors, ambulances, patients, analytics, emergency

# Create tables if not exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Smart Ambulance Dispatch System API",
    description="DSA-2 College Project Backend with Python & FastAPI",
    version="1.0.0"
)

# Enable CORS for React frontend (Vite default: http://localhost:5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
app.include_router(auth.router)
app.include_router(hospitals.router)
app.include_router(doctors.router)
app.include_router(ambulances.router)
app.include_router(patients.router)
app.include_router(analytics.router)
app.include_router(emergency.router)

@app.get("/")
def read_root():
    return {
        "system": "Smart Ambulance Dispatch System API",
        "status": "Online",
        "documentation": "/docs"
    }
