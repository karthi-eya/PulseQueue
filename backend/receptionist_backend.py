from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# -------------------------
# CORS
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CORE_BACKEND_URL = "http://localhost:8000"

# -------------------------
# View Queue
# -------------------------
@app.get("/queue")
def get_queue():
    try:
        response = requests.get(f"{CORE_BACKEND_URL}/queue")
        return response.json()
    except:
        return {"error": "Failed to fetch queue"}

# -------------------------
# Mark Arrival
# -------------------------
@app.post("/arrive/{token}")
def mark_arrival(token: str):
    try:
        response = requests.post(f"{CORE_BACKEND_URL}/arrive/{token}")
        return response.json()
    except:
        return {"error": "Arrival update failed"}

# -------------------------
# Get All Patients
# -------------------------
@app.get("/patients")
def get_all_patients():
    try:
        response = requests.get(f"{CORE_BACKEND_URL}/all-patients")
        return response.json()
    except:
        return {"error": "Failed to fetch patients"}

# -------------------------
# Search Patient
# -------------------------
@app.get("/patient/{token}")
def get_patient(token: str):
    try:
        response = requests.get(f"{CORE_BACKEND_URL}/patient/{token}")
        return response.json()
    except:
        return {"error": "Patient not found"}

# -------------------------
# Estimated Wait Time
# -------------------------
@app.get("/wait-time/{token}")
def wait_time(token: str):
    try:
        response = requests.get(f"{CORE_BACKEND_URL}/queue")
        queue = response.json()

        avg_time_per_patient = 10

        for p in queue:
            if p["token"] == token:
                position = p["queue_number"]   # ✅ FIXED
                wait_time = (position - 1) * avg_time_per_patient

                return {
                    "token": token,
                    "queue_position": position,
                    "estimated_wait_minutes": wait_time,
                    "assigned_doctor": p["doctor"]
                }

        return {"message": "Patient not in queue yet"}

    except:
        return {"error": "Wait time calculation failed"}

# -------------------------
# Dashboard Summary
# -------------------------
@app.get("/dashboard")
def dashboard_summary():
    try:
        response = requests.get(f"{CORE_BACKEND_URL}/queue")
        queue = response.json()

        total_waiting = len(queue)

        doctors = {}
        for p in queue:
            d = p["doctor"]
            doctors[d] = doctors.get(d, 0) + 1

        return {
            "total_waiting": total_waiting,
            "doctor_load": doctors
        }

    except:
        return {"error": "Dashboard failed"}

# -------------------------
# Add Walk-in Patient
# -------------------------
@app.post("/add-patient")
def add_patient(data: dict):
    try:
        response = requests.post(f"{CORE_BACKEND_URL}/add-patient", json=data)
        return response.json()
    except:
        return {"error": "Add patient failed"}