from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional, Annotated


class Patient(BaseModel):

    name: str = Field(max_length=50)  # max_length = maximum length of the string
    age: int = Field(gt=0, lt=140)  # gt = greater than, lt = less than
    weight: Annotated[float, Field(gt=0, strict=True)]
    married: bool
    gender: Annotated[bool, Field(default=True, description="the patient is male")]
    allergies: Optional[List[str]] = None
    contact_details: Dict[str, str] = Field(max_length=5)
    email: EmailStr
    linkendin_url: (
        AnyUrl  # this is a URL field which can ignore complex regex validation
    )
    about: Annotated[
        str,
        Field(
            min_length=10,
            max_length=100,
            description="This patient is from india",
            title="About Patient",
            example=["Patient is from India"],
        ),
    ]


def insert_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print("inserted patient data")


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
    "age": 30,
    "weight": 70.99,
    "married": True,
    "gender": True,
    "contact_details": {"phone": "1234567890"},
    "email": "abc@gmail.com",
    "linkendin_url": "https://www.linkedin.com/in/johndoe/",
    "about": "This patient is from India",
}

patient = Patient(**patient_info)
# print(patient)

# insert_patient_data(patient)
update_patient_data(patient)
