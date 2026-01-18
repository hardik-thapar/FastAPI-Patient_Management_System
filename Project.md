# main.py

The **main.py** file serves as the entry point for the Patient Management API. It uses FastAPI to expose CRUD operations for patient data stored in a local JSON file. The file defines data models, utility functions, and HTTP endpoints.

## Imports

This section lists the external libraries and modules that **main.py** depends on.

- **FastAPI**: Web framework for building APIs  
- **Path**, **HTTPException**: Parameter validation and error handling  
- **JSONResponse**: Custom JSON responses  
- **Pydantic**: BaseModel, Field, computed_field for data validation  
- **typing**: Annotated, Literal, Optional for type hints  
- **json**: Read/write JSON files  

## Data Models 🏥

This part defines the Pydantic models used to validate and serialize patient data.

### Patient

The `Patient` model represents a full patient record. It includes computed properties for BMI and condition.

```python
class Patient(BaseModel):
    id: Annotated[str, Field(description='Enter the ID of the patient',
                             examples=['P1','P2'])]
    name: Annotated[str, Field(description='Enter the Name of the patient',
                               examples=['Rahul', 'Vijay'])]
    age: Annotated[int, Field(gt=0, lt=100, description='Enter the age')]
    gender: Annotated[Literal['male','female','other'],
                     Field(description='Enter the Gender')]
    weight: Annotated[float, Field(gt=0, description='Enter the weight (Kg)')]
    height: Annotated[float, Field(gt=0, description='Enter the Height (in m)')]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi

    @computed_field
    @property
    def condition(self) -> str:
        if self.bmi < 18.5:
            return "underweight"
        if 18.5 < self.bmi < 24.5:
            return "normal"
        return "obese"
```

- **Fields**: `id`, `name`, `age`, `gender`, `weight`, `height`  
- **Computed**:  
  - `bmi`: Body Mass Index  
  - `condition`: Weight category  

### PatientUpdate

The `PatientUpdate` model allows partial updates. All fields are optional.

```python
class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]
```

- Enables PATCH-like behavior via PUT  
- Only provided fields will update existing records  

## Utility Functions 🔧

These functions handle data persistence by reading from and writing to **patients.json**.

### load_data

Loads all patient records from the JSON file.

```python
def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
    return data
```

- Returns a dictionary of patient entries  

### save_data

Writes the updated patient dictionary back to the JSON file.

```python
def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)
```

- Overwrites existing file contents  

## FastAPI Application

An instance of FastAPI powers the API endpoints defined below.

```python
app = FastAPI()
```

## API Endpoints

Below are the available routes for managing patient data. Each endpoint includes its own interactive API block.

### GET /

Returns a simple welcome message.

```api
{
    "title": "Welcome Message",
    "description": "Returns a welcome message for the Patient Management API",
    "method": "GET",
    "baseUrl": "http://localhost:8000",
    "endpoint": "/",
    "headers": [],
    "queryParams": [],
    "pathParams": [],
    "bodyType": "none",
    "responses": {
        "200": {
            "description": "Success",
            "body": "\"Welcome -  Patient Management INFO\""
        }
    }
}
```

### GET /about

Provides a brief description of the platform.

```api
{
    "title": "About Information",
    "description": "Describes the Patient Management and retrieval platform",
    "method": "GET",
    "baseUrl": "http://localhost:8000",
    "endpoint": "/about",
    "headers": [],
    "queryParams": [],
    "pathParams": [],
    "bodyType": "none",
    "responses": {
        "200": {
            "description": "Success",
            "body": "\"Thsi is patient retreival and management platform.\""
        }
    }
}
```

### GET /view

Fetches all patient records.

```api
{
    "title": "List Patients",
    "description": "Retrieves all stored patient records",
    "method": "GET",
    "baseUrl": "http://localhost:8000",
    "endpoint": "/view",
    "headers": [],
    "queryParams": [],
    "pathParams": [],
    "bodyType": "none",
    "responses": {
        "200": {
            "description": "Success",
            "body": "{\n  \"P1\": { \"name\": \"Harry\", \"city\": null, \"age\": 45, \"gender\": \"male\", \"height\": 1.72, \"weight\": 78.0 }\n}"
        }
    }
}
```

### GET /view/{id}

Retrieves a single patient by **id**.

```api
{
    "title": "Get Patient",
    "description": "Fetches details for a specific patient",
    "method": "GET",
    "baseUrl": "http://localhost:8000",
    "endpoint": "/view/{id}",
    "headers": [],
    "queryParams": [],
    "pathParams": [
        {
            "key": "id",
            "value": "Patient ID",
            "required": true
        }
    ],
    "bodyType": "none",
    "responses": {
        "200": {
            "description": "Success",
            "body": "{\n  \"name\": \"Ananya Verma\",\n  \"age\": 29,\n  \"gender\": \"female\",\n  \"weight\": 60,\n  \"height\": 1.65,\n  \"bmi\": 22.0,\n  \"condition\": \"normal\"\n}"
        },
        "404": {
            "description": "Not Found",
            "body": "{\n  \"detail\": \"Patient Not FOUND!\"\n}"
        }
    }
}
```

### POST /createp

Creates a new patient record.

```api
{
    "title": "Create Patient",
    "description": "Adds a new patient to the system",
    "method": "POST",
    "baseUrl": "http://localhost:8000",
    "endpoint": "/createp",
    "headers": [],
    "queryParams": [],
    "pathParams": [],
    "bodyType": "json",
    "requestBody": "{\n  \"id\": \"P8\",\n  \"name\": \"John Doe\",\n  \"age\": 30,\n  \"gender\": \"male\",\n  \"weight\": 70,\n  \"height\": 1.75\n}",
    "responses": {
        "201": {
            "description": "Created",
            "body": "\"Patient Succesfully Created\""
        },
        "400": {
            "description": "Bad Request",
            "body": "{\n  \"detail\": \"Patient Already Exists\"\n}"
        }
    }
}
```

### PUT /edit/{patient_id}

Updates fields for an existing patient.

```api
{
    "title": "Update Patient",
    "description": "Modifies one or more attributes of a patient",
    "method": "PUT",
    "baseUrl": "http://localhost:8000",
    "endpoint": "/edit/{patient_id}",
    "headers": [],
    "queryParams": [],
    "pathParams": [
        {
            "key": "patient_id",
            "value": "Patient ID",
            "required": true
        }
    ],
    "bodyType": "json",
    "requestBody": "{\n  \"city\": \"New York\",\n  \"weight\": 75\n}",
    "responses": {
        "200": {
            "description": "Success",
            "body": "\"Succesfully Updated Patient Patient: P1\""
        },
        "400": {
            "description": "Bad Request",
            "body": "\"Patient doesnt exist\""
        }
    }
}
```

### DELETE /delete/{patient_id}

Removes a patient record permanently.

```api
{
    "title": "Delete Patient",
    "description": "Deletes the patient entry with the given ID",
    "method": "DELETE",
    "baseUrl": "http://localhost:8000",
    "endpoint": "/delete/{patient_id}",
    "headers": [],
    "queryParams": [],
    "pathParams": [
        {
            "key": "patient_id",
            "value": "Patient ID",
            "required": true
        }
    ],
    "bodyType": "none",
    "responses": {
        "200": {
            "description": "Success",
            "body": "\"Patient Succesfully DELETED!\""
        },
        "400": {
            "description": "Bad Request",
            "body": "{\n  \"detail\": \"Patient Not Found!\"\n}"
        }
    }
}
```

## File Relationships

This module interacts primarily with **patients.json**:

- **Read**: `load_data()` retrieves existing records.  
- **Write**: `save_data()` commits updates and deletions.  

No other source files or external databases are involved.