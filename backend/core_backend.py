from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import time

# ✅ Import AUTH (ONLY ONE SYSTEM)
from auth import router as auth_router, SECRET_KEY, ALGORITHM

app = FastAPI(title="PulseQueue API", version="2.0")

# ✅ Mount auth routes
app.include_router(auth_router, prefix="/auth", tags=["auth"])

# -------------------------
# JWT DEPENDENCY (OPTIONAL FOR NOW)
# -------------------------
_bearer = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(_bearer)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

# -------------------------
# CORS (ALLOW FRONTEND)
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# IN-MEMORY STORAGE
# -------------------------
patients = []

AGING_FACTOR = 0.1

# -------------------------
# KEYWORD-BASED SCORING
# -------------------------
KEYWORD_SCORES = {
    "chest pain": 40,
    "unconscious": 50,
    "bleeding": 45,
    "breathing problem": 45,
    "high fever": 30,
    "vomiting": 20,
    "pregnant": 25
}

# -------------------------
# CALCULATE SEVERITY
# -------------------------
def calculate_severity(data):
    score = 0
    symptoms = data.get("symptoms", {})

    if symptoms.get("fever") and isinstance(symptoms["fever"], dict):
        temp = symptoms["fever"].get("temperature", 98)
        days = symptoms["fever"].get("days", 0)
        if temp > 102:
            score += 30
        elif temp > 100:
            score += 20
        score += days * 2

    if symptoms.get("cough") and isinstance(symptoms["cough"], dict):
        score += symptoms["cough"].get("days", 0) * 2

    if symptoms.get("vomiting") and isinstance(symptoms["vomiting"], dict):
        score += 15 + symptoms["vomiting"].get("days", 0) * 2

    if symptoms.get("headache"):
        score += 10

    if symptoms.get("pregnancy"):
        score += 25

    description = data.get("description", "").lower()
    for keyword, value in KEYWORD_SCORES.items():
        if keyword in description:
            score += value

    if score >= 80:
        return 1000

    return score

# -------------------------
# RISK LEVEL
# -------------------------
def get_risk_level(score):
    if score >= 80:
        return "HIGH"
    elif score >= 40:
        return "MEDIUM"
    else:
        return "LOW"

# -------------------------
# DOCTOR ASSIGNMENT
# -------------------------
def assign_doctor(data):
    description = data.get("description", "").lower()
    symptoms = data.get("symptoms", {})

    if symptoms.get("pregnancy") or "pregnant" in description:
        return "Gynecologist"
    elif "chest" in description or "heart" in description:
        return "Cardiologist"
    elif "headache" in description or symptoms.get("headache"):
        return "Neurologist"
    else:
        return "General Physician"

# -------------------------
# ADD PATIENT (NO AUTH FOR NOW → FAST)
# -------------------------
@app.post("/add_patient")
@app.post("/add-patient")
def add_patient(data: dict):
    severity = calculate_severity(data)
    token = f"A{100 + len(patients) + 1}"

    patient = {
        "id": len(patients) + 1,
        "token": token,
        "name": data.get("name", "Unknown"),
        "age": data.get("age", 0),
        "gender": data.get("gender", "Unspecified"),
        "symptoms": data.get("symptoms", {}),
        "description": data.get("description", ""),
        "severity": severity,
        "base_score": severity,
        "priority": float(severity),
        "risk_level": get_risk_level(severity),
        "doctor": assign_doctor(data),
        "arrival_time": time.time(),
        "status": "waiting",
        "arrived": False
    }

    patients.append(patient)

    return {
        "message": "Patient added",
        "patient": patient,
        "token": token
    }

# -------------------------
# BOOK APPOINTMENT
# -------------------------
@app.post("/book")
def book_patient(data: dict):
    return add_patient(data)

# -------------------------
# VIEW QUEUE
# -------------------------
@app.get("/queue")
def get_queue():
    current_time = time.time()

    active = [p for p in patients if p["status"] == "waiting" and p["arrived"]]

    active.sort(
        key=lambda p: p["severity"] + (current_time - p["arrival_time"]) * AGING_FACTOR,
        reverse=True
    )

    for i, p in enumerate(active):
        p["queue_number"] = i + 1
        p["position"] = i + 1
        p["priority"] = p["severity"] + (current_time - p["arrival_time"]) * AGING_FACTOR
        p["estimated_wait"] = i * 5

    return active

# -------------------------
# ALL PATIENTS
# -------------------------
@app.get("/all-patients")
def get_all_patients():
    return patients

# -------------------------
# PATIENT BY TOKEN
# -------------------------
@app.get("/patient/{token}")
def get_patient(token: str):
    for p in patients:
        if str(p["token"]) == str(token) or str(p["id"]) == str(token):
            return p
    return {"error": "Patient not found"}

# -------------------------
# DOCTOR QUEUE
# -------------------------
@app.get("/doctor/{doctor_name}")
def doctor_queue(doctor_name: str):
    current_time = time.time()

    active = [
        p for p in patients
        if p["status"] == "waiting"
        and p["arrived"]
        and p["doctor"].lower() == doctor_name.lower()
    ]

    active.sort(
        key=lambda p: p["severity"] + (current_time - p["arrival_time"]) * AGING_FACTOR,
        reverse=True
    )

    return {
        "doctor": doctor_name,
        "queue": active,
        "total_waiting": len(active)
    }

# -------------------------
# NEXT PATIENT
# -------------------------
@app.post("/next/{doctor_name}")
def next_patient(doctor_name: str):
    current_time = time.time()

    active = [
        p for p in patients
        if p["status"] == "waiting"
        and p["arrived"]
        and p["doctor"].lower() == doctor_name.lower()
    ]

    active.sort(
        key=lambda p: p["severity"] + (current_time - p["arrival_time"]) * AGING_FACTOR,
        reverse=True
    )

    if not active:
        return {"message": "No patients in queue"}

    next_p = active[0]
    next_p["status"] = "done"

    return {
        "message": f"Calling {next_p['name']}",
        "patient": next_p
    }

# -------------------------
# MARK ARRIVED
# -------------------------
@app.post("/arrive/{token}")
def mark_arrived(token: str):
    for p in patients:
        if str(p["token"]) == str(token) or str(p["id"]) == str(token):
            p["arrived"] = True
            p["arrival_time"] = time.time()
            return {"message": "Arrival updated", "token": token}

    return {"error": "Patient not found"}

# -------------------------
# COMPLETE PATIENT
# -------------------------
@app.post("/complete/{token}")
def complete_patient(token: str):
    for p in patients:
        if str(p["token"]) == str(token) or str(p["id"]) == str(token):
            p["status"] = "done"
            return {"message": "Patient completed"}

    return {"error": "Patient not found"}