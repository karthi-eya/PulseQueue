from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Dict
import time

app = FastAPI()

# -------------------------
# In-memory storage
# -------------------------
patients = []
token_counter = 100
AGING_FACTOR = 1  # priority aging per minute


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
    "chest pain": 50,
    "breathing": 50,
    "shortness of breath": 50,
    "difficulty breathing": 50,
    "dizziness": 20,
    "bleeding": 60,
    "internal bleeding": 70,
    "unconscious": 80,
    "fainting": 60,
    "severe pain": 40,
    "sharp pain": 30,
    "pressure": 20,
    "tightness": 30,
    "palpitations": 40,
    "irregular heartbeat": 50,
    "high fever": 40,
    "persistent cough": 20,
    "vomiting blood": 70,
    "blood in stool": 70,
    "weakness": 20,
    "fatigue": 15,
    "blurred vision": 30,
    "loss of vision": 60,
    "speech difficulty": 60,
    "paralysis": 80,
    "numbness": 50,
    "seizure": 80,
    "convulsions": 80,
    "head injury": 70,
    "trauma": 70,
    "burn": 50,
    "infection": 30,
    "swelling": 20,
    "dehydration": 30,
    "diarrhea": 20,
    "persistent vomiting": 40,
    "abdominal pain": 30,
    "severe headache": 40,
    "migraine": 30,
    "sinus": 20,
    "coughing blood": 70,
    "breathlessness": 50
}


# -------------------------
# Severity Calculation
# -------------------------
def calculate_severity(data: PatientInput):
    score = 0

    # Fever
    if data.symptoms.fever:
        temp = data.symptoms.fever.get("temp", 98)
        if temp > 102:
            score += 40
        elif temp > 99:
            score += 20

    # Cough
    if data.symptoms.cough:
        if data.symptoms.cough.get("type") == "wet":
            score += 15
        else:
            score += 10

    # Headache
    if data.symptoms.headache:
        if data.symptoms.headache.get("type") == "migraine":
            score += 25
        elif data.symptoms.headache.get("type") == "sinus":
            score += 15

    # Vomiting
    if data.symptoms.vomiting:
        days = data.symptoms.vomiting.get("days", 0)
        score += days * 5

    # Duration boost
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

    # Gender context
    if data.gender.lower() == "female" and data.symptoms.pregnancy:
        score += 40

    # Genetic disease
    if data.genetic_disease:
        disease = data.genetic_disease.lower()
        if "diabetes" in disease:
            score += 20
        elif "heart" in disease:
            score += 40

    # NLP Description
    desc = data.description.lower()
    for keyword, val in KEYWORD_SCORES.items():
        if keyword in desc:
            score += val

    return score


# -------------------------
# Book Patient
# -------------------------
@app.post("/book")
def book_patient(data: PatientInput):
    global token_counter

    base_score = calculate_severity(data)
    doctor = assign_doctor(data.symptoms)

    token = f"A{token_counter}"
    token_counter += 1

    patient = {
        "token": token,
        "name": data.name,
        "age": data.age,
        "gender": data.gender,
        "symptoms": data.symptoms.dict(),
        "doctor": doctor,
        "base_score": base_score,
        "arrival_time": None,
        "arrived": False
    }

    patients.append(patient)

    return {
        "message": "Appointment confirmed",
        "token": token,
        "assigned_doctor": doctor
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
            return {"message": f"{token} marked as arrived"}

    return {"error": "Patient not found"}


# -------------------------
# Get Queue
# -------------------------
@app.get("/queue")
def get_queue():
    active = [p for p in patients if p["arrived"]]
    current_time = time.time()

    for p in active:
        wait_time = (current_time - p["arrival_time"]) / 60
        p["priority"] = p["base_score"] + wait_time * AGING_FACTOR

    sorted_queue = sorted(active, key=lambda x: x["priority"], reverse=True)

    result = []
    for i, p in enumerate(sorted_queue):
        result.append({
            "token": p["token"],
            "name": p["name"],
            "doctor": p["doctor"],
            "position": i + 1,
            "priority": round(p["priority"], 2)
        })

    return result


# -------------------------
# Get Doctor Queue
# -------------------------
@app.get("/doctor/{doctor_name}")
def doctor_queue(doctor_name: str):
    queue = get_queue()
    doctor_queue = [p for p in queue if p["doctor"] == doctor_name]

    return {
        "doctor": doctor_name,
        "total_waiting": len(doctor_queue),
        "queue": doctor_queue
    }


# -------------------------
# Serve Next Patient
# -------------------------
@app.post("/next/{doctor_name}")
def next_patient(doctor_name: str):
    queue = get_queue()
    doctor_queue = [p for p in queue if p["doctor"] == doctor_name]

    if not doctor_queue:
        return {"message": "No patients for this doctor"}

    next_token = doctor_queue[0]["token"]

    global patients
    patients = [p for p in patients if p["token"] != next_token]

    return {"serving": next_token}


# -------------------------
# Get Patient Details
# -------------------------
@app.get("/patient/{token}")
def get_patient(token: str):
    for p in patients:
        if p["token"] == token:
            return p

    return {"error": "Patient not found"}


# -------------------------
# Get All Patients
# -------------------------
@app.get("/all-patients")
def all_patients():
    return patients