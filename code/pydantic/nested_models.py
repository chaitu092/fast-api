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
print(patient)

print(patient.address.street)
print(patient.address.city)
print(patient.address.state)
print(patient.address.zip_code)
print(patient.name)

# better organization of related data (e.g., address)
# reusability of models (e.g., Address can be reused in other models)
# readability and maintainability of code: easier to understand the structure of the data
# validation of nested data: Pydantic will validate the Address model when creating a Patient instance
