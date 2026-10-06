import math
import uuid
from datetime import datetime
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Hospital, Ambulance, Doctor, Patient, Emergency, Dispatch
from app.schemas import (
    EmergencyCreate, DispatchResultResponse, AmbulanceResponse, 
    HospitalResponse, DoctorResponse, PatientResponse, RouteOption
)

# Import DSA Modules
from app.dsa.graph import Graph
from app.dsa.dijkstra import dijkstra_shortest_path, generate_candidate_routes
from app.dsa.priority_queue import EmergencyPriorityQueue
from app.dsa.kmp import kmp_search
from app.dsa.edit_distance import fuzzy_search_patient
from app.dsa.bipartite import MaximumBipartiteMatching
from app.dsa.dinic import verify_hospital_bed_capacity_flow

router = APIRouter(prefix="/api/emergency", tags=["emergency"])

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)


@router.post("/dispatch", response_model=DispatchResultResponse)
def dispatch_emergency(payload: EmergencyCreate, db: Session = Depends(get_db)):
    """
    MAIN EMERGENCY DISPATCH PIPELINE INTEGRATING DSA ALGORITHMS
    """
    # ------------------------------------------------------------------
    # STEP 1 & DSA CONCEPT C: PRIORITY QUEUE HANDLING
    # ------------------------------------------------------------------
    pq = EmergencyPriorityQueue()
    pq.push({
        "patient_name": payload.patient_name,
        "age": payload.age,
        "emergency_type": payload.emergency_type,
        "latitude": payload.latitude,
        "longitude": payload.longitude
    })
    priority_data = pq.pop()
    calculated_priority = priority_data.get("priority", "Normal")

    # ------------------------------------------------------------------
    # STEP 2 & DSA CONCEPTS F & G: PATIENT RECORD SEARCH (KMP & EDIT DISTANCE)
    # ------------------------------------------------------------------
    all_patients = db.query(Patient).all()
    matched_patient = None
    match_method = None

    # Try KMP Exact Match
    for p in all_patients:
        if kmp_search(p.name, payload.patient_name) or kmp_search(payload.patient_name, p.name):
            matched_patient = p
            match_method = "KMP String Matching (Exact Match)"
            break

    # Fallback to Edit Distance Fuzzy Match
    if not matched_patient:
        fuzzy_p, dist = fuzzy_search_patient(all_patients, payload.patient_name, max_distance=3)
        if fuzzy_p:
            matched_patient = fuzzy_p
            match_method = f"Edit Distance Dynamic Programming (Distance={dist})"

    # If no match, register new patient
    if not matched_patient:
        patient_code = f"P{1000 + len(all_patients) + 1}"
        matched_patient = Patient(
            patient_id=patient_code,
            name=payload.patient_name,
            age=payload.age,
            phone=payload.phone,
            medical_history=f"Created via Emergency Dispatch ({payload.emergency_type})"
        )
        db.add(matched_patient)
        db.commit()
        db.refresh(matched_patient)
        match_method = "New Patient Created"

    # ------------------------------------------------------------------
    # STEP 3: FIND AVAILABLE AMBULANCES & SELECT NEAREST
    # ------------------------------------------------------------------
    available_ambulances = db.query(Ambulance).filter(Ambulance.status == "Available").all()

    if not available_ambulances:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Emergency Dispatch Failed: All 6 ambulance units are currently busy/dispatched!"
        )

    # Calculate distance to each available ambulance
    nearest_ambulance = None
    min_amb_dist = float('inf')

    for amb in available_ambulances:
        dist = haversine_km(payload.latitude, payload.longitude, amb.latitude, amb.longitude)
        if dist < min_amb_dist:
            min_amb_dist = dist
            nearest_ambulance = amb

    # Update ambulance status -> Dispatched
    nearest_ambulance.status = "Dispatched"

    # ------------------------------------------------------------------
    # STEP 4: HOSPITAL FILTERING (CRITICAL: REMOVE ZERO-BED HOSPITALS FIRST!)
    # ------------------------------------------------------------------
    all_hospitals = db.query(Hospital).all()

    # Rule: Hospitals with available_beds == 0 MUST NOT BE SELECTED!
    eligible_hospitals = [h for h in all_hospitals if h.available_beds > 0]

    if not eligible_hospitals:
        nearest_ambulance.status = "Available"  # Revert ambulance
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Emergency Dispatch Failed: No nearby hospitals currently have available beds (> 0)!"
        )

    # Rank/filter by specialization match
    matching_spec_hospitals = [
        h for h in eligible_hospitals 
        if payload.emergency_type.lower() in h.specializations.lower()
    ]
    
    candidate_hospitals = matching_spec_hospitals if matching_spec_hospitals else eligible_hospitals

    # ------------------------------------------------------------------
    # STEP 5 & DSA CONCEPTS A & B: ROAD GRAPH & DIJKSTRA'S ALGORITHM
    # ------------------------------------------------------------------
    graph = Graph()
    graph.build_hyderabad_network(candidate_hospitals)
    user_node = graph.connect_user_location(payload.latitude, payload.longitude)

    # Create mapping of hospital node names to database Hospital objects
    hosp_nodes_map = {f"HOSPITAL_{h.id}": h for h in candidate_hospitals}

    # Run Dijkstra candidate route finder
    candidate_routes = generate_candidate_routes(graph, user_node, hosp_nodes_map)

    if not candidate_routes:
        # Fallback straight distance if graph disconnection
        candidate_routes = []
        for idx, h in enumerate(candidate_hospitals, start=1):
            dist = haversine_km(payload.latitude, payload.longitude, h.latitude, h.longitude)
            eta = max(3, int(dist * 2.2))
            candidate_routes.append({
                "route_id": idx,
                "hospital": h,
                "distance_km": dist,
                "eta_minutes": eta,
                "path_nodes": ["USER_LOCATION", f"HOSPITAL_{h.id}"],
                "coord_path": [[payload.latitude, payload.longitude], [h.latitude, h.longitude]]
            })
        candidate_routes.sort(key=lambda x: x["distance_km"])

    # Selected optimal route & hospital
    optimal_route_info = candidate_routes[0]
    selected_hospital = optimal_route_info["hospital"]

    # Deduct 1 bed from selected hospital
    selected_hospital.available_beds = max(0, selected_hospital.available_beds - 1)

    # ------------------------------------------------------------------
    # STEP 6 & DSA CONCEPT E: BIPARTITE MATCHING FOR DOCTOR ASSIGNMENT
    # ------------------------------------------------------------------
    hospital_doctors = db.query(Doctor).filter(Doctor.hospital_id == selected_hospital.id).all()
    bipartite_matcher = MaximumBipartiteMatching(hospital_doctors, payload.emergency_type)
    assigned_doctor = bipartite_matcher.find_doctor_for_emergency()

    # ------------------------------------------------------------------
    # STEP 7 & DSA CONCEPT D: MAX FLOW / DINIC'S ALGORITHM VERIFICATION
    # ------------------------------------------------------------------
    dinic_flow_result = verify_hospital_bed_capacity_flow(all_hospitals)

    # ------------------------------------------------------------------
    # STEP 8: SAVE EMERGENCY & DISPATCH TO DATABASE
    # ------------------------------------------------------------------
    emergency_code = f"EMG-{uuid.uuid4().hex[:6].upper()}"
    emergency_record = Emergency(
        emergency_code=emergency_code,
        patient_name=payload.patient_name,
        age=payload.age,
        emergency_type=payload.emergency_type,
        latitude=payload.latitude,
        longitude=payload.longitude,
        priority=calculated_priority,
        status="Dispatched"
    )
    db.add(emergency_record)
    db.flush()

    dispatch_record = Dispatch(
        emergency_id=emergency_record.id,
        ambulance_id=nearest_ambulance.id,
        hospital_id=selected_hospital.id,
        doctor_id=assigned_doctor.id if assigned_doctor else None,
        route_info=f"Selected Route 1 ({optimal_route_info['distance_km']} km, {optimal_route_info['eta_minutes']} min)",
        eta_minutes=optimal_route_info["eta_minutes"],
        status="Active"
    )
    db.add(dispatch_record)

    db.commit()
    db.refresh(emergency_record)
    db.refresh(dispatch_record)

    # Format route options for JSON response
    formatted_routes = []
    for idx, r in enumerate(candidate_routes[:3], start=1):
        formatted_routes.append(RouteOption(
            id=idx,
            name=f"Route {idx} ({'Optimal Expressway' if idx==1 else 'Outer Corridor' if idx==2 else 'Inner City Bypass'})",
            distance_km=r["distance_km"],
            eta_minutes=r["eta_minutes"],
            is_recommended=(idx == 1),
            path=r["coord_path"],
            traffic_level="Light" if idx==1 else "Moderate"
        ))

    # Structured DSA Explanation for Review 3 Presentation
    dsa_explanation = {
        "A_Graph_Representation": f"Built Road Graph with {len(graph.adj)} vertices (Hyderabad intersections & hospitals) and weighted edges.",
        "B_Dijkstra_Algorithm": f"Dijkstra computed optimal path to {selected_hospital.hospital_name} with total distance {optimal_route_info['distance_km']} km and ETA {optimal_route_info['eta_minutes']} mins.",
        "C_Priority_Queue": f"Priority Queue evaluated '{payload.emergency_type}' emergency -> assigned '{calculated_priority}' Priority.",
        "D_Dinic_Max_Flow": f"Dinic's algorithm verified hospital network total capacity of {dinic_flow_result['max_flow_bed_capacity']} beds. Zero-bed hospitals had 0 flow capacity.",
        "E_Bipartite_Matching": f"Bipartite Matching assigned Doctor '{assigned_doctor.name if assigned_doctor else 'General Emergency'}' ({assigned_doctor.specialization if assigned_doctor else 'N/A'}) to patient.",
        "F_KMP_String_Matching": f"KMP algorithm searched patient database for '{payload.patient_name}'. Result: {match_method}.",
        "G_Edit_Distance_DP": f"Edit Distance DP evaluated fuzzy match fallback for patient record identity verification."
    }

    return DispatchResultResponse(
        dispatch_id=dispatch_record.id,
        emergency_code=emergency_code,
        emergency_status="AMBULANCE DISPATCHED",
        priority=calculated_priority,
        ambulance=AmbulanceResponse.model_validate(nearest_ambulance),
        hospital=HospitalResponse.model_validate(selected_hospital),
        assigned_doctor=DoctorResponse.model_validate(assigned_doctor) if assigned_doctor else None,
        existing_patient_record=PatientResponse.model_validate(matched_patient),
        match_method=match_method,
        selected_route=formatted_routes[0],
        alternative_routes=formatted_routes,
        dsa_explanation=dsa_explanation
    )
