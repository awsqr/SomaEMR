from http import HTTPStatus
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

db = {7: 'healthy',
      12: 'sick',
      17: 'healthy'}

app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

@app.get('/')
def read_root(request: Request):
    return templates.TemplateResponse(
        'index.html',
        {'request': request,
         'title': 'Soma EMR Home'}
    )

@app.get('/login')
def login(request: Request):
    return templates.TemplateResponse(
        'index.html',
        {'request': request,
         'title': 'Soma EMR Login'}
    )

@app.get('/records/{patient_id}')
def get_record(patient_id: int):
    return JSONResponse(
        content={f'patient number {patient_id}': db.get(patient_id)},
        status_code=HTTPStatus.OK
    )

@app.post('/records/{patient_id}')
def add_patient(patient_id: int, status: str):
    global db
    if (patient_id in db):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                            detail="Invalid ID")
    db[patient_id] = status
    return JSONResponse(
        content={'patient_id': patient_id, "status": status},
        status_code=HTTPStatus.CREATED
    )

@app.put('/records/{patient_id}')
def update_record(patient_id:int, status: str):
    if (patient_id in db):
        db[patient_id] = status
        return {'patient_id': patient_id, "status": status}

    raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

