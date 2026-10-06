# SMART AMBULANCE DISPATCH SYSTEM (DSA-2 Project)

An automated Smart Ambulance Dispatch System built with **Python FastAPI**, **React (Vite)**, **SQLite**, **Leaflet (OpenStreetMap)**, and custom **Data Structures & Algorithms (DSA)** for Review 3 presentation.

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- Python 3.10+
- Node.js v18+ & npm

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Initialize & Seed SQLite Database with 6 ambulances & Hyderabad hospitals
python app/seed.py

# Run FastAPI Backend Server
python run.py
# Backend API running on http://127.0.0.1:8000 (Swagger docs at http://127.0.0.1:8000/docs)
```

### 3. Frontend Setup
```bash
# Open a new terminal and navigate to frontend directory
cd frontend

# Install dependencies (if not already installed)
npm install

# Start Vite React Dev Server
npm run dev
# Frontend app running on http://localhost:5173
```

---

## 🛠️ Technology Stack

- **Frontend**: React, Vite, JavaScript, HTML/CSS, Lucide-React icons, Leaflet & OpenStreetMap.
- **Backend**: Python 3.13, FastAPI, Uvicorn, SQLAlchemy ORM, Pydantic v2.
- **Database**: SQLite (`ambulance_system.db`).

---

## 🧮 Data Structures & Algorithms (DSA) Implementation

| DSA Concept | File Location | Purpose in Application |
|---|---|---|
| **Graph Representation** | `backend/app/dsa/graph.py` | Represents Hyderabad road network (intersections = Vertices, roads = Edges, distance/time = Weights). |
| **Dijkstra's Algorithm** | `backend/app/dsa/dijkstra.py` | Computes optimal shortest route from user location to eligible hospital with alternative candidate routes. |
| **Priority Queue (`heapq`)** | `backend/app/dsa/priority_queue.py` | Prioritizes emergencies based on type (Chest Pain/Breathing -> High, Accident -> High, Other -> Normal). |
| **KMP String Matching** | `backend/app/dsa/kmp.py` | Searches existing patient database for exact substring matches in $O(N+M)$ time. |
| **Edit Distance (DP)** | `backend/app/dsa/edit_distance.py` | Dynamic Programming Levenshtein distance for fuzzy search when exact KMP matching finds no results. |
| **Bipartite Matching** | `backend/app/dsa/bipartite.py` | Augmenting path algorithm matching emergency patients to available specialized doctors at the chosen hospital. |
| **Max Flow / Dinic's Algorithm** | `backend/app/dsa/dinic.py` | Evaluates hospital network bed capacities. Hospitals with 0 beds have 0 flow capacity. |

---

## 👨‍💼 Admin Login Credentials

- **Username**: `admin`
- **Password**: `admin123`

---

## 📋 Demonstration Scenario for Review 3

1. **Admin Login**: Log into Admin Dashboard (`admin` / `admin123`).
2. **Initial State Verification**:
   - See **6 predefined ambulances**: **3 Available** (A01, A02, A03) and **3 Busy** (A04, A05, A06).
   - View real Hyderabad hospitals (Apollo Jubilee Hills, Yashoda Secunderabad, KIMS Begumpet, Continental Gachibowli, Care Banjara Hills, Sunshine Gachibowli).
   - Notice **Continental Hospitals** has `available_beds = 0`.
3. **Report Emergency**:
   - Open User Emergency Form.
   - Click "Detect Location" (uses Browser Geolocation API with fallback).
   - Enter Patient Name (e.g., `Rahul Kumar`), Age (`34`), and select Emergency Type (`Chest Pain`).
   - Click **[ REQUEST AMBULANCE ]**.
4. **Automated Dispatch Execution**:
   - System prioritizes emergency via Priority Queue.
   - System finds nearest Available ambulance (**A01**) and changes status to **Dispatched**.
   - System filters hospitals, **strictly rejecting Continental Hospitals** (`beds = 0`).
   - **Dijkstra's algorithm** computes optimal shortest path (**Route 1**) and alternative candidate routes.
   - **Bipartite matching** assigns an available Cardiology doctor (`Dr. K. Srinivas`).
   - **KMP algorithm** identifies existing patient record for `Rahul Kumar`.
5. **Interactive Map & Results**: View Leaflet map with user position, ambulance location, hospital target, and polyline route.
6. **Completion**: Click **[ Complete Emergency & Free Ambulance ]** to return ambulance status back to **Available**.
