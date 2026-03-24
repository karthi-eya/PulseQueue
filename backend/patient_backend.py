from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Dict
import time
import requests

app = FastAPI()

# Main system backend URL (Queue Server / Reception Backend)
CORE_BACKEND_URL = "http://localhost:8000"

# -------------------------
# Models
# -------------------------
class Symptoms(BaseModel):
    cough: Optional[Dict] = None
    fever: Optional[Dict] = None
    headache: Optional[Dict] = None
    vomiting: Optional[Dict] = None
    pregnancy: Optional[bool] = False


class PatientInput(BaseModel):
    name: str
    age: int
    gender: str
    symptoms: Symptoms
    genetic_disease: Optional[str] = None
    description: Optional[str] = ""


# -------------------------
# Book Appointment
# -------------------------
@app.post("/book")
def book_patient(data: PatientInput):
    """
    Patient books appointment.
    This forwards data to core backend.
    """
    response = requests.post(
        f"{CORE_BACKEND_URL}/book",
        json=data.dict()
    )

    return response.json()


# -------------------------
# Check Queue Position
# -------------------------
@app.get("/queue/{token}")
def check_queue(token: str):
    """
    Patient checks their queue position
    """
    response = requests.get(f"{CORE_BACKEND_URL}/queue")
    queue = response.json()

    for p in queue:
        if p["token"] == token:
            return {
                "token": token,
                "position": p["position"],
                "assigned_doctor": p["doctor"],
                "priority": p["priority"]
            }

    return {"message": "Not in queue yet (arrive at hospital first)"}


# -------------------------
# Estimated Wait Time
# -------------------------
@app.get("/wait-time/{token}")
def estimated_wait(token: str):
    """
    Estimate wait time based on queue position
    """
    response = requests.get(f"{CORE_BACKEND_URL}/queue")
    queue = response.json()

    avg_time_per_patient = 10  # minutes

    for p in queue:
        if p["token"] == token:
            position = p["position"]
            wait_time = (position - 1) * avg_time_per_patient

            return {
                "token": token,
                "estimated_wait_minutes": wait_time,
                "assigned_doctor": p["doctor"]
            }

    return {"message": "Arrive at hospital to enter queue"}


# -------------------------
# Patient Dashboard
# -------------------------
@app.get("/dashboard/{token}")
def patient_dashboard(token: str):
    """
    Patient dashboard info
    """
    queue_response = requests.get(f"{CORE_BACKEND_URL}/queue")
    queue = queue_response.json()

    avg_time_per_patient = 10

    for p in queue:
        if p["token"] == token:
            position = p["position"]
            wait_time = (position - 1) * avg_time_per_patient

            return {
                "token": token,
                "queue_position": position,
                "assigned_doctor": p["doctor"],
                "estimated_wait_minutes": wait_time,
                "priority": p["priority"]
            }

    return {
        "message": "You are booked but not yet arrived",
        "token": token
    }

# -------------------------
# Auth
# -------------------------
@app.post("/signup")
def signup(data: dict):
    response = requests.post(f"{CORE_BACKEND_URL}/signup", json=data)
    return response.json()

@app.post("/login")
def login(data: dict):
    response = requests.post(f"{CORE_BACKEND_URL}/login", json=data)
    return response.json()