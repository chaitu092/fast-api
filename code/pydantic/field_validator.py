from pydantic import BaseModel, AnyUrl, EmailStr, field_validator
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

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        """
        Validate the email field to check if the domain is valid.
        example: @gmail.com, @yahoo.com, @outlook.com"""

        valid_domains = ["gmail.com", "yahoo.com", "outlook.com"]

        # abc@gmail.com
        domain_name = value.split("@")[-1]

        if domain_name not in valid_domains:
            raise ValueError("Invalid email domain")
        return value

    @field_validator("name")
    @classmethod
    def transform_name(cls, value):
        """
        Transform the name field to uppercase.
        example: John Doe -> JOHN DOE
        """
        return value.upper()

    # @field_validator("age", mode="before")
    # @classmethod
    # def validate_age(cls, value):
    #     """
    #     Validate the age field to check if the value is between 0 and 140.
    #     before validation: 30 means
    #     before says before type conversion
    #     it will take only int and if it is a string in the data
    #     it will throw an error
    #     """

    #     if 0 < value < 140:
    #         return value
    #     else:
    #         raise ValueError("Age must be between 0 and 140")

    @field_validator(
        "age", mode="after"
    )  # field validator will validate only on single field
    @classmethod
    def validate_age_after(cls, value):
        """
        Validate the age field to check if the value is between 0 and 140.
        after validation: 30 means
        after says after type conversion
        it will take str and if it is a string also in the data
        it will pass the validation
        """

        if 0 < value < 140:
            return value
        else:
            raise ValueError("Age must be between 0 and 140")


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
    "age": "30",
    "weight": 70.99,
    "married": True,
    "gender": True,
    "allergies": ["pollen", "dust"],
    "contact_details": {"phone": "1234567890"},
    "email": "abc@outlook.com",
    "linkendin_url": "https://www.linkedin.com/in/johndoe/",
    "about": "This patient is from India",
}

patient = Patient(**patient_info)
# print(patient)

# insert_patient_data(patient)
update_patient_data(patient)
