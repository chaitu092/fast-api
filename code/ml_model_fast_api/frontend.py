import streamlit as st
import requests


API_URL = "http://localhost:8000/predict"  # Adjust the URL as needed


st.title("Health Insurance Premium Prediction")
st.sidebar.title("Health Insurance Premium Prediction")
st.markdown(
    """
    This application predicts the health insurance premium based on user inputs.
    Please fill in the details below to get your premium prediction.
    """
)

# User inputs
age = st.number_input("Age", min_value=0, max_value=120, value=30)
height = st.number_input("Height (in meters)", min_value=0.5, max_value=3.0, value=1.75)
weight = st.number_input("Weight (in kg)", min_value=30, max_value=200, value=70)
smoker = st.selectbox("Are you a smoker?", ["Yes", "No"])
smoker = "yes" if smoker == "Yes" else "no"
income_lpa = st.number_input("Annual Income (in LPA)", min_value=0, value=5)
occupation = st.selectbox(
    "Occupation",
    [
        "freelancer",
        "government_job",
        "unemployed",
        "student",
        "retired",
        "private_job",
        "business_owner",
    ],
    index=0,
)
city = st.text_input("City", value="Hyderabad")

if st.button("Predict Premium"):
    payload = {
        "age": age,
        "height": height,
        "weight": weight,
        "smoker": smoker,
        "income_lpa": income_lpa,
        "occupation": occupation,
        "city": city,
    }

    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()  # Raise an error for bad responses
        prediction = response.json()
        st.success(f"Predicted Premium: ₹{prediction['premium']}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")
    except ValueError:
        st.error("Invalid response from the server.")
