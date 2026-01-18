from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel, Field, computed_field
from fastapi.responses import JSONResponse
from typing import Annotated, Literal, Optional
import json

# "P1": {
#     "name": "Rahul Sharma",
#     "age": 45,
#     "gender": "male",
#     "weight": 78,
#     "height": 1.72,
#     "bmi": 26.4,
#     "condition": "obese"

class Patient(BaseModel):
    id: Annotated[str, Field(..., description='Enter the ID of the patient', examples=['P1','P2'])]
    name: Annotated[str, Field(...,description='Enter the Name of the patient', examples=['Rahul', 'Vijay'])]
    age: Annotated[int, Field(..., gt=0, lt=100, description='Enter the age')]
    gender: Annotated[Literal['male','female','other'], Field(..., description='Enter the Gender')]
    weight: Annotated[float, Field(..., gt=0, description='Enter the weight (Kg)')]
    height: Annotated[float, Field(..., gt=0, description='Enter the Height (in m)')]

@computed_field
@property
def bmi(self)->float:
   bmi=round(self.weight/(self.height**2),2)
   return bmi

@computed_field
@property
def condition(self)->str:
   bmi=self.bmi

   if(bmi<18.5):
      return "underweight"
   if(18.5<bmi<24.5):
      return "normal"
   return "obese"

class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]


def load_data(): 
    with open('patients.json', 'r') as f:
     data = json.load(f)
     return data

def save_data(data):
    with open('patients.json','w') as f:
       json.dump(data,f)

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
def view_patient(id: str = Path(..., description ="Enter the patient ID here", examples=["P2"])):
   data = load_data()

   if id in data:
      return data[id]
   raise HTTPException(status_code=404, detail='Patient Not FOUND!')

@app.post('/createp')
def create_patient(patient: Patient):
   #load data
   data = load_data()
    #check if patient already exists
   if patient.id in data:
      raise HTTPException(status_code=400, detail='Patient Already Exists')
   #add new data
   data[patient.id]=patient.model_dump(exclude=['id'])
   save_data(data)
   return JSONResponse(status_code=201, content='Patient Succesfully Created')
   
@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):
#    load the data
    data = load_data()
    # check if patient exist or not
    if patient_id not in data:
       raise HTTPException(status_code=400, content="Patient doesnt exist")
   
    existing_patient_info=data[patient_id]
    updated_patient_info=patient_update.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
       existing_patient_info[key]=value

    existing_patient_info['id']=patient_id

    #create a pydantic obj to calculate new bmi and condition if any
    patient_pydantic_obj = PatientUpdate(**existing_patient_info)
    # convert back to dict
    existing_patient_info=patient_pydantic_obj.model_dump(exclude='id')

    data[patient_id]=existing_patient_info
    save_data(data)

    return JSONResponse(status_code=200, content=f"Succesfully Updated Patient Patient: {patient_id}")