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
# Get Doctor Queue
# -------------------------
@app.get("/queue/{doctor_name}")
def doctor_queue(doctor_name: str):
    response = requests.get(f"{CORE_BACKEND_URL}/doctor/{doctor_name}")
    return response.json()


# -------------------------
# Get Current Patient
# -------------------------
@app.get("/current/{doctor_name}")
def current_patient(doctor_name: str):
    response = requests.get(f"{CORE_BACKEND_URL}/doctor/{doctor_name}")
    data = response.json()

    if data["queue"]:
        return {
            "current_patient": data["queue"][0],
            "waiting_count": data["total_waiting"]
        }

    return {"message": "No patients waiting"}


# -------------------------
# Call Next Patient
# -------------------------
@app.post("/next/{doctor_name}")
def next_patient(doctor_name: str):
    response = requests.post(f"{CORE_BACKEND_URL}/next/{doctor_name}")
    return response.json()


# -------------------------
# Get Patient Details
# -------------------------
@app.get("/patient/{token}")
def patient_details(token: str):
    response = requests.get(f"{CORE_BACKEND_URL}/patient/{token}")
    return response.json()


# -------------------------
# Doctor Dashboard Summary
# -------------------------
@app.get("/dashboard/{doctor_name}")
def doctor_dashboard(doctor_name: str):
    response = requests.get(f"{CORE_BACKEND_URL}/doctor/{doctor_name}")
    data = response.json()

    if not data["queue"]:
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