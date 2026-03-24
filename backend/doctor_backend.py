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

CORE_BACKEND_URL = "http://127.0.0.1:8000"

# -------------------------
# Get Doctor Queue
# -------------------------
@app.get("/queue/{doctor_name}")
def doctor_queue(doctor_name: str):
    try:
        response = requests.get(f"{CORE_BACKEND_URL}/doctor/{doctor_name}")
        return response.json()
    except:
        return {"error": "Core backend not reachable"}

# -------------------------
# Get Current Patient
# -------------------------
@app.get("/current/{doctor_name}")
def current_patient(doctor_name: str):
    try:
        response = requests.get(f"{CORE_BACKEND_URL}/doctor/{doctor_name}")
        data = response.json()

        if "queue" in data and data["queue"]:
            return {
                "current_patient": data["queue"][0],
                "waiting_count": data["total_waiting"]
            }

        return {"current_patient": None, "waiting_count": 0}

    except:
        return {"error": "Failed to fetch current patient"}

# -------------------------
# Call Next Patient
# -------------------------
@app.post("/next/{doctor_name}")
def next_patient(doctor_name: str):
    try:
        response = requests.post(f"{CORE_BACKEND_URL}/next/{doctor_name}")
        return response.json()
    except:
        return {"error": "Failed to call next patient"}

# -------------------------
# Get Patient Details
# -------------------------
@app.get("/patient/{token}")
def patient_details(token: str):
    try:
        response = requests.get(f"{CORE_BACKEND_URL}/patient/{token}")
        return response.json()
    except:
        return {"error": "Patient fetch failed"}

# -------------------------
# Doctor Dashboard Summary
# -------------------------
@app.get("/dashboard/{doctor_name}")
def doctor_dashboard(doctor_name: str):
    try:
        response = requests.get(f"{CORE_BACKEND_URL}/doctor/{doctor_name}")
        data = response.json()

        if "queue" not in data or not data["queue"]:
            return {
                "doctor": doctor_name,
                "current_patient": None,
                "waiting_patients": 0
            }

        return {
            "doctor": doctor_name,
            "current_patient": data["queue"][0],
            "waiting_patients": data["total_waiting"]
        }

    except:
        return {"error": "Dashboard load failed"}