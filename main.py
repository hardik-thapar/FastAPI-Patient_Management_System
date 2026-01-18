from fastapi import FastAPI, Path, HTTPException, Queue
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
import json

# "P1": {
#     "name": "Rahul Sharma",
#     "age": 45,
#     "gender": "male",
#     "weight": 78,
#     "height": 1.72,
#     "bmi": 26.4,
#     "condition": "obese"

class Patient():
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

@app.get("/sort")
def sorted(sort_by: str = Queue(...,description="choose from ")):
   pass
   
