import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

from app.seed import seed_database

def test_endpoints():
    print("Seeding database...")
    seed_database()
    print("Testing GET / ...")
    r = client.get("/")
    assert r.status_code == 200
    print("Root Endpoint:", r.json())

    print("\nTesting GET /api/hospitals ...")
    r = client.get("/api/hospitals")
    assert r.status_code == 200
    hospitals = r.json()
    print(f"Loaded {len(hospitals)} hospitals")

    print("\nTesting GET /api/ambulances ...")
    r = client.get("/api/ambulances")
    assert r.status_code == 200
    ambulances = r.json()
    print(f"Loaded {len(ambulances)} ambulances")
    available_count = len([a for a in ambulances if a['status'] == 'Available'])
    busy_count = len([a for a in ambulances if a['status'] == 'Busy'])
    print(f"Available ambulances: {available_count}, Busy ambulances: {busy_count}")
    assert available_count == 3, "Should have 3 available ambulances"
    assert busy_count == 3, "Should have 3 busy ambulances"

    print("\nTesting POST /api/emergency/dispatch ...")
    payload = {
        "patient_name": "Rahul Kumar",
        "age": 34,
        "emergency_type": "Chest Pain",
        "latitude": 17.4320,
        "longitude": 78.4050,
        "phone": "9876543210"
    }
    r = client.post("/api/emergency/dispatch", json=payload)
    assert r.status_code == 200
    dispatch_res = r.json()
    print("Dispatch Result Summary:")
    print("  Ambulance:", dispatch_res["ambulance"]["ambulance_code"], dispatch_res["ambulance"]["status"])
    print("  Hospital:", dispatch_res["hospital"]["hospital_name"], f"(Beds: {dispatch_res['hospital']['available_beds']})")
    print("  Assigned Doctor:", dispatch_res["assigned_doctor"]["name"] if dispatch_res["assigned_doctor"] else "None")
    print("  Match Method:", dispatch_res["match_method"])
    print("  Recommended Route:", dispatch_res["selected_route"]["name"], f"({dispatch_res['selected_route']['distance_km']} km, ETA {dispatch_res['selected_route']['eta_minutes']} min)")

    print("\nBACKEND API INTEGRATION TEST SUCCESSFUL!")

if __name__ == "__main__":
    test_endpoints()
