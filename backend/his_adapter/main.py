import httpx
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class HIS_Patient(BaseModel):
    # Default fields
    name: str
    age: int
    diagnosis: str
    
    # Allow any additional fields
    class Config:
        extra = "allow"

# patients = [
#     {"name": "John Doe", "age": 45, "diagnosis": "Hypertension"},
#     {"name": "Jane Smith", "age": 37, "diagnosis": "Diabetes"},
# ]


# @app.on_event("startup")
# async def import_patients():
#     async with httpx.AsyncClient() as client:
#         try:
#             response = await client.post(
#                 "http://patient:8000/patients/import", json=patients
#             )
#             print(response.json())
#         except httpx.RequestError as e:
#             print(f"Failed to import patients: {e}")


@app.get("/")
async def root():
    return {"message": "HIS-Adapter is running"}

@app.post("/his-adapter/import")
async def imports(his_patients: List[HIS_Patient]):
    async with httpx.AsyncClient() as client:
        # TODO: Unify different client data structure
        patients = [patient.dict() for patient in his_patients]
        try:
            response = await client.post(
                "http://patient:8000/patients/import", json=patients
            )
            print(response.json())
        except httpx.RequestError as e:
            print(f"Failed to import patients: {e}")


# @app.get("/his-adapter/import")
# async def import_patients():
#     async with httpx.AsyncClient() as client:
#         try:
#             response = await client.post("http://patient:8000/patients/import", json=patients)
#             print(response.json())
#         except httpx.RequestError as e:
#             print(f"Failed to import patients: {e}")
