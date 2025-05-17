from fastapi import FastAPI
import json

app = FastAPI()


# loading the data from a JSON file
def load_patient_data():
    with open("patients.json", "r") as file:
        patient_data = json.load(file)
    return patient_data


@app.get("/")
def patient():
    return {"Message": "Welcome to the Patient Management System"}


@app.get("/patients_details")
def patients_details():
    return {"Message": "This endpoint will return the details of all patients."}


@app.get("/patient_view")
def patient_view():
    patient_data = load_patient_data()
    return {"patients": patient_data}
