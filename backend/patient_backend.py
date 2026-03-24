from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    try:
        response = requests.post(
            f"{CORE_BACKEND_URL}/book",
            json=data.dict()
        )
        return response.json()
    except:
        return {"error": "Backend not reachable"}

# -------------------------
# Check Queue Position
# -------------------------
@app.get("/queue/{token}")
def check_queue(token: str):
    try:
        response = requests.get(f"{CORE_BACKEND_URL}/queue")
        queue = response.json()

        for p in queue:
            if p["token"] == token:
                return {
                    "token": token,
                    "position": p["queue_number"],   # ✅ FIXED
                    "assigned_doctor": p["doctor"],
                    "priority": p["priority"]
                }

        return {
            "status": "not_arrived",
            "message": "Arrive at hospital to enter queue"
        }

    except:
        return {"error": "Queue fetch failed"}

# -------------------------
# Estimated Wait Time
# -------------------------
@app.get("/wait-time/{token}")
def estimated_wait(token: str):
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
                    "estimated_wait_minutes": wait_time,
                    "assigned_doctor": p["doctor"]
                }

        return {"message": "Arrive at hospital to enter queue"}

    except:
        return {"error": "Wait time fetch failed"}

# -------------------------
# Patient Dashboard
# -------------------------
@app.get("/dashboard/{token}")
def patient_dashboard(token: str):
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
                    "assigned_doctor": p["doctor"],
                    "estimated_wait_minutes": wait_time,
                    "priority": p["priority"]
                }

        return {
            "status": "booked_not_arrived",
            "message": "You are booked but not yet arrived",
            "token": token
        }

    except:
        return {"error": "Dashboard failed"}

# -------------------------
# Auth
# -------------------------
@app.post("/signup")
def signup(data: dict):
    try:
        response = requests.post(f"{CORE_BACKEND_URL}/signup", json=data)
        return response.json()
    except:
        return {"error": "Signup failed"}

@app.post("/login")
def login(data: dict):
    try:
        response = requests.post(f"{CORE_BACKEND_URL}/login", json=data)
        return response.json()
    except:
        return {"error": "Login failed"}