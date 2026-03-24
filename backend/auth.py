from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from jose import jwt
from datetime import datetime, timedelta

router = APIRouter()

SECRET_KEY = "pulsequeue_secret_2026"
ALGORITHM = "HS256"
TOKEN_EXPIRE_HOURS = 8

# -------------------------
# HARDCODED STAFF CREDENTIALS (NO HASHING → FAST)
# -------------------------
users_db: dict = {
    "general":   {"password": "doc@123", "role": "doctor", "specialty": "General Physician"},
    "cardio":    {"password": "doc@123", "role": "doctor", "specialty": "Cardiologist"},
    "derma":     {"password": "doc@123", "role": "doctor", "specialty": "Dermatologist"},
    "neuro":     {"password": "doc@123", "role": "doctor", "specialty": "Neurologist"},
    "ent":       {"password": "doc@123", "role": "doctor", "specialty": "ENT"},
    "8121017003": {"password": "reception@123", "role": "reception", "specialty": None},
}

# -------------------------
# PATIENT DB (in-memory)
# -------------------------
patients_db: dict = {}

# -------------------------
# MODELS
# -------------------------
class LoginRequest(BaseModel):
    user_id: str
    password: str

class SignupRequest(BaseModel):
    name: str
    age: int
    password: str

# -------------------------
# HELPERS
# -------------------------
def create_token(data: dict) -> str:
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(hours=TOKEN_EXPIRE_HOURS)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def _redirect_for_role(role: str) -> str:
    if role == "doctor":
        return "/doctor/dist/index.html"
    if role == "reception":
        return "/receptionist/dashboard.html"
    return "/patient/symptoms.html"

# -------------------------
# SIGNUP (patients only)
# -------------------------
@router.post("/signup")
def signup(data: SignupRequest):
    user_id = f"patient{len(patients_db) + 1}"

    patients_db[user_id] = {
        "name": data.name,
        "age": data.age,
        "password": data.password,  # plain text for speed
        "role": "patient",
    }

    return {
        "message": "Signup successful",
        "user_id": user_id
    }

# -------------------------
# LOGIN (all roles)
# -------------------------
@router.post("/login")
def login(data: LoginRequest):
    uid = data.user_id.strip()
    pwd = data.password.strip()

    print("Login request received for:", uid)

    # --- Staff (doctors / receptionist) ---
    if uid in users_db:
        user = users_db[uid]

        if pwd != user["password"]:
            raise HTTPException(status_code=401, detail="Incorrect password")

        token = create_token({
            "user_id": uid,
            "role": user["role"],
            "specialty": user.get("specialty"),
        })

        return {
            "token": token,
            "role": user["role"],
            "specialty": user.get("specialty"),
            "redirect": _redirect_for_role(user["role"]),
        }

    # --- Patients ---
    if uid in patients_db:
        user = patients_db[uid]

        if pwd != user["password"]:
            raise HTTPException(status_code=401, detail="Incorrect password")

        token = create_token({
            "user_id": uid,
            "role": "patient"
        })

        return {
            "token": token,
            "role": "patient",
            "name": user["name"],
            "redirect": _redirect_for_role("patient"),
        }

    raise HTTPException(
        status_code=404,
        detail="User not found. Please sign up first."
    )