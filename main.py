from fastapi import FastAPI, Path, HTTPException
import json

def load_data():
    with open('patients.json', 'r') as f:
     data = json.load(f)
     return data

app = FastAPI()

@app.get('/')
def hello():
    return {'Welcome -  Patient Management INFO'}

@app.get('/about')
def about():
    return {'Thsi is patient retreival and management platform.'}

@app.get('/view')
def view():
   data = load_data()
   return data

@app.get('/view/{id}')
def view_patient(id: str = Path(..., description ="Enter the patient ID here", example="P2")):
   data = load_data()

   if id in data:
      return data[id]
   raise HTTPException(status_code=404, detail='Patient Not FOUND!')
