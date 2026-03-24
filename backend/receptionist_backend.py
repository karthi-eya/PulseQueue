from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CORE_BACKEND_URL = "http://localhost:8000"


# -------------------------
# View Queue (for receptionist dashboard table)
# -------------------------
@app.get("/queue")
def get_queue():
    response = requests.get(f"{CORE_BACKEND_URL}/queue")
    return response.json()


# -------------------------
# Mark Patient Arrival
# -------------------------
@app.post("/arrive/{token}")
def mark_arrival(token: str):
    response = requests.post(f"{CORE_BACKEND_URL}/arrive/{token}")
    return response.json()


# -------------------------
# Get All Patients (Booked + Arrived)
# -------------------------
@app.get("/patients")
def get_all_patients():
    response = requests.get(f"{CORE_BACKEND_URL}/all-patients")
    return response.json()


# -------------------------
# Search Patient by Token
# -------------------------
@app.get("/patient/{token}")
def get_patient(token: str):
    response = requests.get(f"{CORE_BACKEND_URL}/patient/{token}")
    return response.json()


# -------------------------
# Estimated Wait Time
# -------------------------
@app.get("/wait-time/{token}")
def wait_time(token: str):
    response = requests.get(f"{CORE_BACKEND_URL}/queue")
    queue = response.json()

    avg_time_per_patient = 10  # minutes

    for p in queue:
        if p["token"] == token:
            position = p["position"]
            wait_time = (position - 1) * avg_time_per_patient

            return {
                "token": token,
                "queue_position": position,
                "estimated_wait_minutes": wait_time,
                "assigned_doctor": p["doctor"]
            }

    return {"message": "Patient not in queue yet"}


# -------------------------
# Dashboard Summary
# -------------------------
@app.get("/dashboard")
def dashboard_summary():
    queue_response = requests.get(f"{CORE_BACKEND_URL}/queue")
    queue = queue_response.json()

    total_waiting = len(queue)

    doctors = {}
    for p in queue:
        d = p["doctor"]
        if d not in doctors:
            doctors[d] = 0
        doctors[d] += 1

    return {
        "total_waiting": total_waiting,
        "doctor_load": doctors
    }

# -------------------------
# Add Walk-in Patient
# -------------------------
@app.post("/add-patient")
def add_patient(data: dict):
    response = requests.post(f"{CORE_BACKEND_URL}/add-patient", json=data)
    return response.json()