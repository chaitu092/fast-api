from pydantic import BaseModel, EmailStr, AnyUrl, computed_field
from typing import Dict, List


class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    weight: float
    height: float
    married: bool
    gender: bool
    allergies: List[str]
    contact_details: Dict[str, str]
    linkendin_url: AnyUrl
    about: str

    @computed_field  # this is a computed field which is not stored in the database, calculated on the fly (derived value)
    @property
    def calculate_bmi(self) -> float:
        """
        Calculate the BMI of the patient.
        """
        bmi = self.weight / (self.height**2)
        return round(bmi, 2)


def update_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.height)
    print("BMI:", patient.calculate_bmi)
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
    "weight": 75.2,
    "height": 1.72,
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
