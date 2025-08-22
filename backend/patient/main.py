from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

class PatientIn(BaseModel):
    name: str
    age: int
    diagnosis: str

@app.post("/patients/import")
def import_patients(patients: List[PatientIn]):
    try:
        conn = psycopg2.connect(
            dbname="medical", user="user", password="pass", host="db"
        )
        cur = conn.cursor()
        for p in patients:
            cur.execute(
                "INSERT INTO patients (name, age, diagnosis) VALUES (%s, %s, %s)",
                (p.name, p.age, p.diagnosis)
            )
        conn.commit()
        return {"status": "imported", "count": len(patients)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
      
@app.get("/patients")
def get_patients():
    try:
        conn = psycopg2.connect(
            dbname="medical", user="user", password="pass", host="db"
        )
        # Use RealDictCursor to get results as dictionaries
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("SELECT * FROM patients")
        patients = cur.fetchall()  # fetch all rows
        
        cur.close()
        conn.close()
        
        return {"patients": patients}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/patients/{patient_id}")
def get_patient(patient_id: int):
    try:
        conn = psycopg2.connect(
            dbname="medical", user="user", password="pass", host="db"
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Use parameterized query to prevent SQL injection
        cur.execute("SELECT * FROM patients WHERE id = %s", (patient_id,))
        patient = cur.fetchone()  # fetch one row
        
        cur.close()
        conn.close()
        
        if patient is None:
            raise HTTPException(status_code=404, detail="Patient not found")
        
        return {"patient": patient}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
