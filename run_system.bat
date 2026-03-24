start cmd /k uvicorn backend.core_backend:app --port 8000 --reload
start cmd /k uvicorn backend.patient_backend:app --port 8001 --reload
start cmd /k uvicorn backend.receptionist_backend:app --port 8002 --reload
start cmd /k uvicorn backend.doctor_backend:app --port 8003 --reload
start cmd /k cd frontend && python -m http.server 5500