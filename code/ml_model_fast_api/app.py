from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
import pandas as pd
import pickle

# load the model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

tier_1_cities = [
    "Mumbai",
    "Delhi",
    "Bangalore",
    "Chennai",
    "Kolkata",
    "Hyderabad",
    "Pune",
]

tier_2_cities = [
    "Jaipur",
    "Chandigarh",
    "Indore",
    "Lucknow",
    "Patna",
    "Ranchi",
    "Visakhapatnam",
    "Coimbatore",
    "Bhopal",
    "Nagpur",
    "Vadodara",
    "Surat",
    "Rajkot",
    "Jodhpur",
    "Raipur",
    "Amritsar",
    "Varanasi",
    "Agra",
    "Dehradun",
    "Mysore",
    "Jabalpur",
    "Guwahati",
    "Thiruvananthapuram",
    "Ludhiana",
    "Nashik",
    "Allahabad",
    "Udaipur",
    "Aurangabad",
    "Hubli",
    "Belgaum",
    "Salem",
    "Vijayawada",
    "Tiruchirappalli",
    "Bhavnagar",
    "Gwalior",
    "Dhanbad",
    "Bareilly",
    "Aligarh",
    "Gaya",
    "Kozhikode",
    "Warangal",
    "Kolhapur",
    "Bilaspur",
    "Jalandhar",
    "Noida",
    "Guntur",
    "Asansol",
    "Siliguri",
]
# Create the FastAPI app
app = FastAPI()


# pydantic model to validate the input data
class UserInput(BaseModel):
    age: Annotated[
        int,
        Field(..., gt=0, lt=110, description="The age of the user", examples=["25"]),
    ]

    weight: Annotated[
        float, Field(..., gt=0, description="The weight of the user", examples=["70"])
    ]
    height: Annotated[
        float,
        Field(
            ..., gt=0, lt=2.5, description="The height of the user", examples=["1.9"]
        ),
    ]
    income_lpa: Annotated[
        float,
        Field(
            ...,
            gt=0,
            description="The income of the user in lakhs per annum",
            examples=["10"],
        ),
    ]
    smoker: Annotated[
        Literal["yes", "no"],
        Field(
            ...,
            description="Whether the user is a smoker or not",
        ),
    ]
    city: Annotated[
        str, Field(..., description="The city of the user", examples=["Hyderabad"])
    ]
    occupation: Annotated[
        Literal[
            "freelancer",
            "government_job",
            "unemployed",
            "student",
            "retired",
            "private_job",
            "business_owner",
        ],
        Field(..., description="The occupation of the user", examples=["private_job"]),
    ]

    @computed_field  # this is a computed field which is not stored in the database, calculated on the fly (derived value)
    @property
    def bmi(self) -> float:
        """
        Calculate the BMI of the patient.
        """
        bmi = self.weight / (self.height**2)
        return bmi

    @computed_field
    @property
    def lifestyle_status(self) -> str:
        """
        Calculate the lifestyle status of the user based on BMI and smoking status.
        """

        if self.smoker and self.bmi > 30:
            return "Unhealthy"
        elif self.smoker and self.bmi <= 27:
            return "Moderately Healthy"
        else:
            return "Healthy"

    @computed_field
    @property
    def age_group(self) -> str:
        """
        Determine the age group of the user based on their age.
        """

        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle-aged"
        else:
            return "senior"

    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return "tier_1"
        elif self.city in tier_2_cities:
            return "tier_2"
        else:
            return "tier_3"


@app.post("/predict")
def predict_premium(data: UserInput):

    input_df = pd.DataFrame(
        [
            {
                "bmi": data.bmi,
                "age_group": data.age_group,
                "lifestyle_status": data.lifestyle_status,
                "city_tier": data.city_tier,
                "income_lpa": data.income_lpa,
                "occupation": data.occupation,
            }
        ]
    )

    prediction = model.predict(input_df)[0]

    return JSONResponse(status_code=200, content={"premium": prediction})
