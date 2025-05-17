from fastapi import FastAPI, Path, HTTPException, Query
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
    """
    This endpoint retrieves the details of all patients.
    return: A dictionary containing a list of all patients.
    """
    patient_data = load_patient_data()
    return {"patients": patient_data}


@app.get("/patient/{patient_id}")
def patient_view_by_id(
    patient_id: str = Path(
        ..., description="ID of the patient in the DB", example="P001"
    )
):
    """
    Path parameters are dynamic segment values in the URL that can be used to retrieve specific resources.

    This endpoint retrieves the details of a specific patient by their ID.
    param patient_id: The ID of the patient to retrieve.
    return: A dictionary containing the patient's details or an error message if not found.
    """
    patient_data = load_patient_data()
    if patient_id in patient_data:
        return patient_data[patient_id]
    raise HTTPException(
        status_code=404,
        detail=f"Patient with ID {patient_id} not found.",
    )


@app.get("/sort")
def sort_patients(
    sort_by: str = Query(..., description="Sort on the basis of height, weight, bmi"),
    order: str = Query("asc", description="sort in asc or desc order"),
):

    patient_data = load_patient_data()

    valid_sort_fields = ["height", "weight", "bmi"]
    if sort_by not in valid_sort_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sort field. Valid fields are: {', '.join(valid_sort_fields)}.",
        )

    if order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=400, detail="Invalid order. Use 'asc' or 'desc'."
        )
    sort_order = True if order == "desc" else False
    sorted_patients = sorted(
        patient_data.values(),
        key=lambda x: x.get(sort_by, 0),  # Default to 0 if the key is not found
        reverse=(sort_order),
    )
    return {"sorted_patients": sorted_patients}
