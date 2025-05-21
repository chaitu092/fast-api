# to export pydantic model objects to python dictionary or JSON

from pydantic import BaseModel


class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str


class Patient(BaseModel):
    name: str
    age: int
    gender: str
    address: Address


address_dict = {
    "street": "123 Main St",
    "city": "New York",
    "state": "NY",
    "zip_code": "10001",
}

address1 = Address(**address_dict)

patient_dict = {"name": "John Doe", "age": 26, "gender": "male", "address": address1}
patient = Patient(**patient_dict)

# dumping the model to a dictionary
# this will convert the model to a dictionary
temp = patient.model_dump(include=["name", "age"])
print(temp)
print(type(temp))


# dumping the model to a JSON
temp = patient.model_dump_json(exclude={"address": ["zip_code"]})
print(temp)
print(type(temp))
