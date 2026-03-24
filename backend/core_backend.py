from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

<<<<<<< HEAD
users = {}  # username -> password
=======
<<<<<<< HEAD
users = {}  # username -> password
=======
users = {} # For patient login: username -> password
>>>>>>> ebd3769429badfa257ba7bbfacbd6b5fcd9faecf
>>>>>>> 5bf515a7459975030f5ec15afd6e1fca23c784f8

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
# Doctor Assignment (5 Specialties)
# General Physician, Cardiologist, Dermatologist, Neurologist, ENT
# -------------------------
<<<<<<< HEAD
CARDIO_KEYWORDS = ["chest pain", "heart", "palpitations", "irregular heartbeat", "blood pressure", "cardiac", "tightness"]
DERMA_KEYWORDS = ["skin", "rash", "acne", "eczema", "itching", "allergy", "hives", "psoriasis", "dermatitis", "boils"]
NEURO_KEYWORDS = ["migraine", "seizure", "convulsions", "paralysis", "numbness", "dizziness", "speech difficulty", "blurred vision"]
ENT_KEYWORDS = ["ear", "nose", "throat", "sinus", "tonsil", "hearing", "snoring", "nasal", "sore throat", "cough"]

def assign_doctor(symptoms, description=""):
    desc = description.lower() if description else ""

    # 1. Check NLP description keywords first (highest specificity)
    for kw in CARDIO_KEYWORDS:
        if kw in desc:
            return "Cardiologist"
    for kw in DERMA_KEYWORDS:
        if kw in desc:
            return "Dermatologist"
    for kw in NEURO_KEYWORDS:
        if kw in desc:
            return "Neurologist"
    for kw in ENT_KEYWORDS:
        if kw in desc:
            return "ENT"

    # 2. Check structured symptom objects
    if symptoms.headache:
        return "Neurologist"

    if symptoms.cough:
        return "ENT"

    if symptoms.pregnancy:
        return "General Physician"

    if symptoms.vomiting:
        return "General Physician"

    if symptoms.fever:
=======
def assign_doctor(symptoms):
    if symptoms.pregnancy:
        return "Gynecologist"
    if symptoms.headache:
        return "Neurologist"
    if symptoms.vomiting:
        return "Gastroenterologist"
    if symptoms.cough or symptoms.fever:
>>>>>>> 5bf515a7459975030f5ec15afd6e1fca23c784f8
        return "General Physician"
    return "General Physician"

# -------------------------
# NLP Keyword Scores
# -------------------------
KEYWORD_SCORES = {
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> 5bf515a7459975030f5ec15afd6e1fca23c784f8
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
=======
    "chest pain": 50, "breathing": 50, "shortness of breath": 50, "difficulty breathing": 50,
    "dizziness": 20, "bleeding": 60, "internal bleeding": 70, "unconscious": 80,
    "fainting": 60, "severe pain": 40, "sharp pain": 30, "pressure": 20, "tightness": 30,
    "palpitations": 40, "irregular heartbeat": 50, "high fever": 40, "persistent cough": 20,
    "vomiting blood": 70, "blood in stool": 70, "weakness": 20, "fatigue": 15,
    "blurred vision": 30, "loss of vision": 60, "speech difficulty": 60, "paralysis": 80,
    "numbness": 50, "seizure": 80, "convulsions": 80, "head injury": 70, "trauma": 70,
    "burn": 50, "infection": 30, "swelling": 20, "dehydration": 30, "diarrhea": 20,
    "persistent vomiting": 40, "abdominal pain": 30, "severe headache": 40,
    "migraine": 30, "sinus": 20, "coughing blood": 70, "breathlessness": 50
>>>>>>> ebd3769429badfa257ba7bbfacbd6b5fcd9faecf
}

# -------------------------
# Severity Calculation
# -------------------------
def calculate_severity(data: PatientInput):
    score = 0
<<<<<<< HEAD

<<<<<<< HEAD
=======
=======
>>>>>>> ebd3769429badfa257ba7bbfacbd6b5fcd9faecf
>>>>>>> 5bf515a7459975030f5ec15afd6e1fca23c784f8
    if data.symptoms.fever:
        temp = data.symptoms.fever.get("temp", 98)
        if temp > 102: score += 40
        elif temp > 99: score += 20
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> 5bf515a7459975030f5ec15afd6e1fca23c784f8

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

<<<<<<< HEAD
=======
=======
    if data.symptoms.cough:
        if data.symptoms.cough.get("type") == "wet": score += 15
        else: score += 10
    if data.symptoms.headache:
        if data.symptoms.headache.get("type") == "migraine": score += 25
        elif data.symptoms.headache.get("type") == "sinus": score += 15
>>>>>>> ebd3769429badfa257ba7bbfacbd6b5fcd9faecf
>>>>>>> 5bf515a7459975030f5ec15afd6e1fca23c784f8
    if data.symptoms.vomiting:
        days = data.symptoms.vomiting.get("days", 0)
        score += days * 5

<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> 5bf515a7459975030f5ec15afd6e1fca23c784f8
    # Duration factor
    total_days = 0
    for s in [data.symptoms.cough, data.symptoms.fever,
              data.symptoms.headache, data.symptoms.vomiting]:
        if s:
            total_days += s.get("days", 0)
<<<<<<< HEAD
=======
=======
    total_days = 0
    for s in [data.symptoms.cough, data.symptoms.fever, data.symptoms.headache, data.symptoms.vomiting]:
        if s: total_days += s.get("days", 0)
>>>>>>> ebd3769429badfa257ba7bbfacbd6b5fcd9faecf
>>>>>>> 5bf515a7459975030f5ec15afd6e1fca23c784f8
    score += total_days * 2

    if data.age < 5: score += 15
    elif data.age > 60: score += 25

<<<<<<< HEAD
    # Pregnancy
=======
<<<<<<< HEAD
    # Pregnancy
=======
>>>>>>> ebd3769429badfa257ba7bbfacbd6b5fcd9faecf
>>>>>>> 5bf515a7459975030f5ec15afd6e1fca23c784f8
    if data.gender.lower() == "female" and data.symptoms.pregnancy:
        score += 40

    if data.genetic_disease:
        disease = data.genetic_disease.lower()
        if "diabetes" in disease: score += 20
        elif "heart" in disease: score += 40

<<<<<<< HEAD
    # NLP description scoring
=======
<<<<<<< HEAD
    # NLP description scoring
=======
>>>>>>> ebd3769429badfa257ba7bbfacbd6b5fcd9faecf
>>>>>>> 5bf515a7459975030f5ec15afd6e1fca23c784f8
    desc = data.description.lower()
    for keyword, val in KEYWORD_SCORES.items():
        if keyword in desc:
            score += val

    return score

# -------------------------
<<<<<<< HEAD
# Auth
=======
<<<<<<< HEAD
# Auth
=======
# User Authentication
>>>>>>> ebd3769429badfa257ba7bbfacbd6b5fcd9faecf
>>>>>>> 5bf515a7459975030f5ec15afd6e1fca23c784f8
# -------------------------
@app.post("/signup")
def signup(data: LoginData):
    if data.username in users:
<<<<<<< HEAD
        return {"success": False, "message": "Username exists"}
    users[data.username] = data.password
    return {"success": True}
=======
<<<<<<< HEAD
        return {"success": False, "message": "Username exists"}
    users[data.username] = data.password
    return {"success": True}
=======
        return {"success": False, "message": "Username already exists"}
    users[data.username] = data.password
    return {"success": True, "message": "Signup successful"}
>>>>>>> ebd3769429badfa257ba7bbfacbd6b5fcd9faecf
>>>>>>> 5bf515a7459975030f5ec15afd6e1fca23c784f8

@app.post("/login")
def login(data: LoginData):
    if data.username in users and users[data.username] == data.password:
<<<<<<< HEAD
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
        "doctor": assign_doctor(data.symptoms, data.description),
        "priority": calculate_severity(data),  # ✅ FIXED
        "arrival_time": time.time(),
        "arrived": True
    }

    patients.append(patient)
    return {"message": "Patient added", "token": token}
=======
<<<<<<< HEAD
        return {"success": True}
    return {"success": False}
>>>>>>> 5bf515a7459975030f5ec15afd6e1fca23c784f8

# -------------------------
# Add Walk-in Patient
=======
        return {"success": True, "message": "Logged in"}
    return {"success": False, "message": "Invalid credentials"}

# -------------------------
# Walk-in Patient / Add
>>>>>>> ebd3769429badfa257ba7bbfacbd6b5fcd9faecf
# -------------------------
@app.post("/add-patient")
def add_patient(data: PatientInput):
    global token_counter
<<<<<<< HEAD

<<<<<<< HEAD
=======
=======
>>>>>>> ebd3769429badfa257ba7bbfacbd6b5fcd9faecf
>>>>>>> 5bf515a7459975030f5ec15afd6e1fca23c784f8
    token_counter += 1
    token = f"A{token_counter}"

    patient = {
        "token": token,
        "name": data.name,
        "age": data.age,
        "gender": data.gender,
        "symptoms": data.symptoms.dict(),
        "doctor": assign_doctor(data.symptoms),
<<<<<<< HEAD
        "priority": calculate_severity(data),
=======
<<<<<<< HEAD
        "priority": calculate_severity(data),  # ✅ FIXED
        "arrival_time": time.time(),
        "arrived": True
    }

    patients.append(patient)
    return {"message": "Patient added", "token": token}
=======
        "priority": 10,
        "arrival_time": time.time(),
        "arrived": True
    }
    patients.append(patient)
    return {"message": "Patient added", "token": token}

>>>>>>> ebd3769429badfa257ba7bbfacbd6b5fcd9faecf

# -------------------------
# Book Patient
# -------------------------
@app.post("/book")
def book_patient(data: PatientInput):
    global token_counter
<<<<<<< HEAD

=======
    base_score = calculate_severity(data)
    doctor = assign_doctor(data.symptoms)

    token = f"A{token_counter}"
>>>>>>> ebd3769429badfa257ba7bbfacbd6b5fcd9faecf
    token_counter += 1
    token = f"A{token_counter}"

    patient = {
        "token": token,
        "name": data.name,
        "age": data.age,
        "gender": data.gender,
        "symptoms": data.symptoms.dict(),
<<<<<<< HEAD
        "doctor": assign_doctor(data.symptoms),
        "priority": calculate_severity(data),
=======
        "doctor": doctor,
        "priority": base_score,
>>>>>>> ebd3769429badfa257ba7bbfacbd6b5fcd9faecf
>>>>>>> 5bf515a7459975030f5ec15afd6e1fca23c784f8
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

<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> 5bf515a7459975030f5ec15afd6e1fca23c784f8
    return {"success": False, "error": "Patient not found"}

=======
>>>>>>> ebd3769429badfa257ba7bbfacbd6b5fcd9faecf
# -------------------------
# Queue
# -------------------------
@app.get("/queue")
def get_queue():
<<<<<<< HEAD
    active = [p for p in patients if p["arrived"]]

    active.sort(
        key=lambda x: -(
            x["priority"] +
            ((time.time() - x["arrival_time"]) / 60) * AGING_FACTOR
        )
    )

<<<<<<< HEAD
=======
=======
    active = [p for p in patients if p["arrived"] and p.get("arrival_time") is not None]
    
    # Sort by priority and time waiting
    active.sort(key=lambda x: -(x["priority"] + (time.time() - x["arrival_time"]) / 60 * AGING_FACTOR))

>>>>>>> ebd3769429badfa257ba7bbfacbd6b5fcd9faecf
>>>>>>> 5bf515a7459975030f5ec15afd6e1fca23c784f8
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
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> 5bf515a7459975030f5ec15afd6e1fca23c784f8

    for p in queue:
        if p["doctor"] == doctor_name:
            patients[:] = [pt for pt in patients if pt["token"] != p["token"]]
            return {"message": "Next patient", "patient": p}

<<<<<<< HEAD
=======
=======
    
    for p in queue:
        if p["doctor"] == doctor_name:
            patients.remove(p)
            return {"message": "Next patient called", "patient": p}
            
>>>>>>> ebd3769429badfa257ba7bbfacbd6b5fcd9faecf
>>>>>>> 5bf515a7459975030f5ec15afd6e1fca23c784f8
    return {"message": "No patients"}

# -------------------------
# Get Patient
# -------------------------
@app.get("/patient/{token}")
def get_patient(token: str):
    for p in patients:
        if p["token"] == token:
            return p
<<<<<<< HEAD
    return {"error": "Not found"}
=======
<<<<<<< HEAD
    return {"error": "Not found"}
=======
    return {"error": "Patient not found"}
>>>>>>> ebd3769429badfa257ba7bbfacbd6b5fcd9faecf
>>>>>>> 5bf515a7459975030f5ec15afd6e1fca23c784f8

# -------------------------
# All Patients
# -------------------------
@app.get("/all-patients")
def all_patients():
    return patients