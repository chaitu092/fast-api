from pydantic import BaseModel, EmailStr, model_validator, AnyUrl
from typing import Dict, List


class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    weight: float
    married: bool
    gender: bool
    allergies: List[str]
    contact_details: Dict[str, str]
    linkendin_url: AnyUrl
    about: str

    @model_validator(mode="after")
    @classmethod
    def validate_emergency_contact(cls, model):

        if model.age > 60 and "emergency" not in model.contact_details:
            raise ValueError("Emergency contact is required for patients above 60")
        return model


def update_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.married)
    print(patient.gender)
    print(patient.allergies)
    print(patient.contact_details)
    print(patient.email)
    print(patient.linkendin_url)
    print(patient.about)
    print("This is all about patient data")


patient_info = {
    "name": "John Doe",
    "age": "69",
    "weight": 70.99,
    "married": True,
    "gender": True,
    "allergies": ["pollen", "dust"],
    "contact_details": {"phone": "1234567890", "emergency": "2200998817"},
    "email": "abc@outlook.com",
    "linkendin_url": "https://www.linkedin.com/in/johndoe/",
    "about": "This patient is from India",
}

patient = Patient(**patient_info)
# print(patient)

# insert_patient_data(patient)
update_patient_data(patient)
