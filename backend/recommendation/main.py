from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Patient(BaseModel):
    id: int
    age: int
    diagnosis: str

@app.post("/recommend")
def recommend(patient: Patient):
    return {
        "recommendations": [
            f"Review treatment plan for diagnosis: {patient.diagnosis}",
            "Check for allergies before prescribing antibiotics"
        ]
    }
