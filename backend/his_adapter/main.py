from fastapi import FastAPI
import httpx

app = FastAPI()

patients = [
  { "name": "John Doe", "age": 45, "diagnosis": "Hypertension" },
  { "name": "Jane Smith", "age": 37, "diagnosis": "Diabetes" }
]

@app.on_event("startup")
async def import_patients():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post("http://patient:8000/patients/import", json=patients)
            print(response.json())
        except httpx.RequestError as e:
            print(f"Failed to import patients: {e}")

@app.get("/")
async def root():
    return {"message": "HIS-Adapter is running"}
  
# @app.get("/his-adapter/import")
# async def import_patients():
#     async with httpx.AsyncClient() as client:
#         try:
#             response = await client.post("http://patient:8000/patients/import", json=patients)
#             print(response.json())
#         except httpx.RequestError as e:
#             print(f"Failed to import patients: {e}")