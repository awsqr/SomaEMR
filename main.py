import requests.exceptions
from fastapi import FastAPI
from requests import HTTPError

app = FastAPI()

db = {7: 'healthy'}

@app.get('/records/{patient_id}')
def get_record(patient_id: int):
    return {f'patient number {patient_id}': db.get(patient_id)}

@app.post('/records/{patient_id}')
def add_patient(patient_id: int, status: str):
    global db
    db[patient_id] = status
    return {'patient_id': patient_id, "status": status}

@app.put('/records/{patient_id}')
def update_record(patient_id:int, status: str):
    if (patient_id in db):
        db[patient_id] = status
        return {'patient_id': patient_id, "status": status}

    return requests.exceptions.HTTPError

