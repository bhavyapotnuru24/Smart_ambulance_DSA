import sys
import os

# Add parent dir to path so app module can be imported when running script directly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import Base, engine, SessionLocal
from app.models import AdminUser, Hospital, Ambulance, Doctor, Patient, Emergency, Dispatch

def seed_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 1. Seed Admin User (admin / admin123)
        admin = AdminUser(username="admin", password_hash="admin123")
        db.add(admin)

        # 2. Seed 6 Predefined Ambulances (3 Available, 3 Busy as specified)
        ambulances = [
            Ambulance(ambulance_code="A01", status="Available", latitude=17.4300, longitude=78.4000, driver_name="Ramesh Kumar", driver_phone="9849012345"),
            Ambulance(ambulance_code="A02", status="Available", latitude=17.4500, longitude=78.4800, driver_name="Suresh Verma", driver_phone="9849012346"),
            Ambulance(ambulance_code="A03", status="Available", latitude=17.4100, longitude=78.4300, driver_name="Venkat Rao", driver_phone="9849012347"),
            Ambulance(ambulance_code="A04", status="Busy", latitude=17.4400, longitude=78.3600, driver_name="Mohammed Ali", driver_phone="9849012348"),
            Ambulance(ambulance_code="A05", status="Busy", latitude=17.4000, longitude=78.4700, driver_name="Krishna Reddy", driver_phone="9849012349"),
            Ambulance(ambulance_code="A06", status="Busy", latitude=17.3800, longitude=78.4800, driver_name="Ganesh Singh", driver_phone="9849012350"),
        ]
        db.add_all(ambulances)

        # 3. Seed Real Hyderabad Hospitals
        hospitals = [
            Hospital(
                hospital_name="Apollo Hospitals, Jubilee Hills",
                address="Road No 72, Jubilee Hills, Hyderabad",
                latitude=17.4265,
                longitude=78.4116,
                specializations="Chest Pain,Breathing Problem,Accident / Injury,Other,Cardiology,Neurology,Emergency,Orthopedics",
                total_beds=100,
                available_beds=12,
                phone="040-23607777"
            ),
            Hospital(
                hospital_name="Yashoda Hospitals, Secunderabad",
                address="Alexander Road, Secunderabad, Hyderabad",
                latitude=17.4435,
                longitude=78.4984,
                specializations="Chest Pain,Breathing Problem,Accident / Injury,Other,Cardiology,Pulmonology,Emergency",
                total_beds=80,
                available_beds=8,
                phone="040-45674567"
            ),
            Hospital(
                hospital_name="KIMS Hospitals, Begumpet",
                address="Minister Road, Begumpet, Secunderabad",
                latitude=17.4411,
                longitude=78.4820,
                specializations="Breathing Problem,Accident / Injury,Other,Emergency,Pulmonology,Pediatrics",
                total_beds=60,
                available_beds=5,
                phone="040-44885000"
            ),
            Hospital(
                hospital_name="Continental Hospitals, Gachibowli",
                address="Financial District, Nanakramguda, Gachibowli, Hyderabad",
                latitude=17.4239,
                longitude=78.3487,
                specializations="Chest Pain,Breathing Problem,Accident / Injury,Other,Cardiology,Oncology,Emergency",
                total_beds=120,
                available_beds=0,  # 0 beds to test zero-bed rejection logic!
                phone="040-67000000"
            ),
            Hospital(
                hospital_name="Care Hospitals, Banjara Hills",
                address="Road No 1, Banjara Hills, Hyderabad",
                latitude=17.4124,
                longitude=78.4485,
                specializations="Chest Pain,Accident / Injury,Other,Cardiology,Emergency,Orthopedics",
                total_beds=75,
                available_beds=15,
                phone="040-61656565"
            ),
            Hospital(
                hospital_name="Sunshine Hospitals, Gachibowli",
                address="Near Bio Diversity Park, Gachibowli, Hyderabad",
                latitude=17.4398,
                longitude=78.3802,
                specializations="Accident / Injury,Other,Orthopedics,Trauma,Emergency",
                total_beds=50,
                available_beds=6,
                phone="040-44550000"
            )
        ]
        db.add_all(hospitals)
        db.commit()

        # Fetch inserted hospitals to map IDs for Doctors
        h1 = db.query(Hospital).filter_by(hospital_name="Apollo Hospitals, Jubilee Hills").first()
        h2 = db.query(Hospital).filter_by(hospital_name="Yashoda Hospitals, Secunderabad").first()
        h3 = db.query(Hospital).filter_by(hospital_name="KIMS Hospitals, Begumpet").first()
        h5 = db.query(Hospital).filter_by(hospital_name="Care Hospitals, Banjara Hills").first()
        h6 = db.query(Hospital).filter_by(hospital_name="Sunshine Hospitals, Gachibowli").first()

        # 4. Seed Doctors with specializations
        doctors = [
            Doctor(name="Dr. K. Srinivas", specialization="Chest Pain", is_available=True, hospital_id=h1.id),
            Doctor(name="Dr. Radhika Sharma", specialization="Breathing Problem", is_available=True, hospital_id=h1.id),
            Doctor(name="Dr. P. V. Ramana", specialization="Accident / Injury", is_available=True, hospital_id=h1.id),
            Doctor(name="Dr. Arvind Swamy", specialization="Chest Pain", is_available=True, hospital_id=h2.id),
            Doctor(name="Dr. Meenakshi Sundaram", specialization="Breathing Problem", is_available=True, hospital_id=h2.id),
            Doctor(name="Dr. Rajesh Nambiar", specialization="Breathing Problem", is_available=True, hospital_id=h3.id),
            Doctor(name="Dr. Sneha Reddy", specialization="Accident / Injury", is_available=True, hospital_id=h3.id),
            Doctor(name="Dr. Mohammed Osman", specialization="Chest Pain", is_available=True, hospital_id=h5.id),
            Doctor(name="Dr. Vikram Malhotra", specialization="Accident / Injury", is_available=True, hospital_id=h6.id),
        ]
        db.add_all(doctors)

        # 5. Seed Patient Records (for KMP & Edit Distance search testing)
        patients = [
            Patient(patient_id="P1001", name="Rahul Kumar", age=34, phone="9876543210", medical_history="Hypertension, Asthma"),
            Patient(patient_id="P1002", name="Apollo Sharma", age=45, phone="9876543211", medical_history="Cardiac Stent (2022)"),
            Patient(patient_id="P1003", name="Ananya Sharma", age=28, phone="9876543212", medical_history="Type 1 Diabetes"),
            Patient(patient_id="P1004", name="Vikram Reddy", age=52, phone="9876543213", medical_history="Coronary Artery Disease"),
        ]
        db.add_all(patients)

        db.commit()
        print("Database initialized & seeded successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
