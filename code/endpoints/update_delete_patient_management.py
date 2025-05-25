from fastapi import FastAPI, Path, HTTPException, Query
from pydantic import BaseModel, Field, computed_field
from fastapi.responses import JSONResponse
from typing import Annotated, Literal, Optional
import json

app = FastAPI()


class Patient(BaseModel):
    id: Annotated[
        str, Field(..., description="The ID of the patient", examples=["P001"])
    ]
    name: Annotated[
        str,
        Field(..., description="The name of the patient", examples=["Arjun Sarkar"]),
    ]
    city: Annotated[
        str, Field(..., description="The city of the patient", examples=["Kolkata"])
    ]
    age: Annotated[
        int,
        Field(..., gt=0, lt=110, description="The age of the patient", examples=["25"]),
    ]
    gender: Annotated[
        Literal["male", "female", "others"],
        Field(
            ...,
            description="Gender of the patient",
        ),
    ]
    height: Annotated[
        float,
        Field(..., gt=0, description="The height of the patient", examples=["1.9"]),
    ]
    weight: Annotated[
        float,
        Field(..., gt=0, description="The weight of the patient", examples=["70"]),
    ]

    @computed_field  # this is a computed field which is not stored in the database, calculated on the fly (derived value)
    @property
    def calculate_bmi(self) -> float:
        """
        Calculate the BMI of the patient.
        """
        bmi = self.weight / (self.height**2)
        return round(bmi, 2)

    @computed_field
    @property
    def verdict(self) -> str:
        """
        Calculate the verdict of the patient.
        """
        if self.calculate_bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.calculate_bmi < 24.9:
            return "Normal weight"
        elif 25 <= self.calculate_bmi < 29.9:
            return "Overweight"
        else:
            return "Obesity"


class UpdatePatient(BaseModel):

    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[
        Optional[int],
        Field(
            default=None,
            gt=0,
            lt=110,
        ),
    ]
    gender: Annotated[
        Optional[
            Literal[
                "male",
                "female",
                "others",
            ]
        ],
        Field(
            default=None,
        ),
    ]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]


def load_patient_data():
    try:
        with open("patients.json", "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return []


def save_patient_data(patients):
    with open("patients.json", "w") as file:
        json.dump(patients, file, indent=4)


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


@app.post("/create_patient")
def create_patient(patient: Patient):
    """
    This endpoint creates a new patient.
    """

    # Load existing patient data
    patients = load_patient_data()

    # Check if patient ID already exists
    if patient.id in patients:
        raise HTTPException(
            status_code=400,
            detail=f"Patient with ID {patient.id} already exists.",
        )

    # Add the new patient to the list
    patients[patient.id] = patient.model_dump(exclude={"id"})

    # Save the updated patient data
    save_patient_data(patients)

    return JSONResponse(
        status_code=201, content={"message": "Patient created successfully"}
    )


@app.put("/edit_patient/{patient_id}")
def update_patient(patient_id: str, patient_update: UpdatePatient):
    """
    This endpoint updates the details of an existing patient.
    """
    # Load existing patient data
    patients = load_patient_data()

    # Check if patient ID exists
    if patient_id not in patients:
        raise HTTPException(
            status_code=404,
            detail=f"Patient with ID {patient_id} not found.",
        )
    # Get the existing patient info
    exisiting_patinet_info = patients[patient_id]

    patient_update__dict_info = patient_update.model_dump(exclude_unset=True)

    for key, value in patient_update__dict_info.items():
        if value is not None:
            exisiting_patinet_info[key] = value
    # existing_patinet_info -> pydantic object -> update bmi + verdict
    exisiting_patinet_info["id"] = patient_id  # Ensure the ID remains unchanged
    patient_pydantic_obj = Patient(**exisiting_patinet_info)
    # -> convert to pydantic object
    exisiting_patinet_info = patient_pydantic_obj.model_dump(
        exclude={"id"}
    )  # Exclude ID from the dump
    # Update the patient info

    patients[patient_id] = exisiting_patinet_info

    # Save the updated patient data
    save_patient_data(patients)
    return JSONResponse(
        status_code=200, content={"message": "Patient updated successfully"}
    )


@app.delete("/delete_patient/{patient_id}")
def delete_patient(patient_id: str):
    """
    This endpoint deletes a patient by their ID.
    """
    # Load existing patient data
    patients = load_patient_data()

    # Check if patient ID exists
    if patient_id not in patients:
        raise HTTPException(
            status_code=404,
            detail=f"Patient with ID {patient_id} not found.",
        )

    # Delete the patient from the list
    del patients[patient_id]

    # Save the updated patient data
    save_patient_data(patients)

    return JSONResponse(
        status_code=200, content={"message": "Patient deleted successfully"}
    )
