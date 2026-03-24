from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict
import time

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

# -------------------------
# In-memory storage
# -------------------------
patients = []
token_counter = 100
AGING_FACTOR = 0.01   # ✅ FIXED (was too high)

users = {}  # username -> password

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

class LoginData(BaseModel):
    username: str
    password: str

# -------------------------
# Doctor Assignment
# -------------------------
def assign_doctor(symptoms):
    if symptoms.pregnancy:
        return "Gynecologist"
    if symptoms.headache:
        return "Neurologist"
    if symptoms.vomiting:
        return "Gastroenterologist"
    if symptoms.cough or symptoms.fever:
        return "General Physician"
    return "General Physician"

# -------------------------
# NLP Keyword Scores
# -------------------------
KEYWORD_SCORES = {
    "chest pain": 50, "breathing": 50, "shortness of breath": 50,
    "difficulty breathing": 50, "dizziness": 20, "bleeding": 60,
    "internal bleeding": 70, "unconscious": 80, "fainting": 60,
    "severe pain": 40, "sharp pain": 30, "pressure": 20,
    "tightness": 30, "palpitations": 40, "irregular heartbeat": 50,
    "high fever": 40, "persistent cough": 20, "vomiting blood": 70,
    "blood in stool": 70, "weakness": 20, "fatigue": 15,
    "blurred vision": 30, "loss of vision": 60,
    "speech difficulty": 60, "paralysis": 80, "numbness": 50,
    "seizure": 80, "convulsions": 80, "head injury": 70,
    "trauma": 70, "burn": 50, "infection": 30, "swelling": 20,
    "dehydration": 30, "diarrhea": 20, "persistent vomiting": 40,
    "abdominal pain": 30, "severe headache": 40,
    "migraine": 30, "sinus": 20, "coughing blood": 70,
    "breathlessness": 50
}

# -------------------------
# Severity Calculation
# -------------------------
def calculate_severity(data: PatientInput):
    score = 0

    if data.symptoms.fever:
        temp = data.symptoms.fever.get("temp", 98)
        if temp > 102: score += 40
        elif temp > 99: score += 20

    if data.symptoms.cough:
        if data.symptoms.cough.get("type") == "wet":
            score += 15
        else:
            score += 10

    if data.symptoms.headache:
        if data.symptoms.headache.get("type") == "migraine":
            score += 25
        elif data.symptoms.headache.get("type") == "sinus":
            score += 15

    if data.symptoms.vomiting:
        days = data.symptoms.vomiting.get("days", 0)
        score += days * 5

    # Duration factor
    total_days = 0
    for s in [data.symptoms.cough, data.symptoms.fever,
              data.symptoms.headache, data.symptoms.vomiting]:
        if s:
            total_days += s.get("days", 0)
    score += total_days * 2

    # Age factor
    if data.age < 5:
        score += 15
    elif data.age > 60:
        score += 25

    # Pregnancy
    if data.gender.lower() == "female" and data.symptoms.pregnancy:
        score += 40

    # Genetic disease
    if data.genetic_disease:
        disease = data.genetic_disease.lower()
        if "diabetes" in disease:
            score += 20
        elif "heart" in disease:
            score += 40

    # NLP description scoring
    desc = data.description.lower()
    for keyword, val in KEYWORD_SCORES.items():
        if keyword in desc:
            score += val

    return score

# -------------------------
# Auth
# -------------------------
@app.post("/signup")
def signup(data: LoginData):
    if data.username in users:
        return {"success": False, "message": "Username exists"}
    users[data.username] = data.password
    return {"success": True}

@app.post("/login")
def login(data: LoginData):
    if data.username in users and users[data.username] == data.password:
        return {"success": True}
    return {"success": False}

# -------------------------
# Add Walk-in Patient
# -------------------------
@app.post("/add-patient")
def add_patient(data: PatientInput):
    global token_counter

    token_counter += 1
    token = f"A{token_counter}"

    patient = {
        "token": token,
        "name": data.name,
        "age": data.age,
        "gender": data.gender,
        "symptoms": data.symptoms.dict(),
        "doctor": assign_doctor(data.symptoms),
        "priority": calculate_severity(data),  # ✅ FIXED
        "arrival_time": time.time(),
        "arrived": True
    }

    patients.append(patient)
    return {"message": "Patient added", "token": token}

# -------------------------
# Book Patient
# -------------------------
@app.post("/book")
def book_patient(data: PatientInput):
    global token_counter

    token_counter += 1
    token = f"A{token_counter}"

    patient = {
        "token": token,
        "name": data.name,
        "age": data.age,
        "gender": data.gender,
        "symptoms": data.symptoms.dict(),
        "doctor": assign_doctor(data.symptoms),
        "priority": calculate_severity(data),
        "arrival_time": None,
        "arrived": False
    }

    patients.append(patient)

    return {
        "message": "Appointment confirmed",
        "token": token,
        "assigned_doctor": patient["doctor"]
    }

# -------------------------
# Mark Arrival
# -------------------------
@app.post("/arrive/{token}")
def mark_arrival(token: str):
    for p in patients:
        if p["token"] == token:
            p["arrived"] = True
            p["arrival_time"] = time.time()
            return {
                "success": True,
                "token": token,
                "arrival_time": p["arrival_time"]
            }

    return {"success": False, "error": "Patient not found"}

# -------------------------
# Queue
# -------------------------
@app.get("/queue")
def get_queue():
    active = [p for p in patients if p["arrived"]]

    active.sort(
        key=lambda x: -(
            x["priority"] +
            ((time.time() - x["arrival_time"]) / 60) * AGING_FACTOR
        )
    )

    for i, p in enumerate(active):
        p["queue_number"] = i + 1

    return active

# -------------------------
# Doctor Queue
# -------------------------
@app.get("/doctor/{doctor_name}")
def doctor_queue(doctor_name: str):
    queue = get_queue()
    doctor_patients = [p for p in queue if p["doctor"] == doctor_name]

    return {
        "queue": doctor_patients,
        "total_waiting": len(doctor_patients)
    }

# -------------------------
# Next Patient
# -------------------------
@app.post("/next/{doctor_name}")
def next_patient(doctor_name: str):
    queue = get_queue()

    for p in queue:
        if p["doctor"] == doctor_name:
            patients[:] = [pt for pt in patients if pt["token"] != p["token"]]
            return {"message": "Next patient", "patient": p}

    return {"message": "No patients"}

# -------------------------
# Get Patient
# -------------------------
@app.get("/patient/{token}")
def get_patient(token: str):
    for p in patients:
        if p["token"] == token:
            return p
    return {"error": "Not found"}

# -------------------------
# All Patients
# -------------------------
@app.get("/all-patients")
def all_patients():
    return patients