import streamlit as st
import joblib
import pandas as pd
import os
import base64

# Page configuration
st.set_page_config(layout="wide", page_title="Car Dheko - Price Prediction", page_icon="🚗")

# Load paths
dataset_path = "Structured_data_set/Processed_dataset.csv"
model_path = "pipeline_model.pkl"

# Custom CSS for layout and style changes
st.markdown("""
    <style>
    /* General body styling */
    body {
        background: linear-gradient(135deg, #1e3c72, #2a5298);
        font-family: 'Roboto', sans-serif;
        color: #ffffff;
    }

    /* Hero section */
    .hero {
        text-align: center;
        padding: 80px 0;
        background: linear-gradient(45deg, #FF7A00, #00BFFF);
        border-radius: 10px;
        margin: 40px 0;
        box-shadow: 0px 4px 30px rgba(0, 0, 0, 0.1);
    }

    .hero h1 {
        font-size: 50px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 10px;
    }

    .hero p {
        font-size: 20px;
        color: #fff;
        margin-bottom: 30px;
    }

    /* Sidebar styling */
    .sidebar-content {
        font-size: 18px;
        color: #00BFFF;
        font-weight: 600;
    }

    /* Sidebar width adjustment */
    .css-1d391kg {  /* Sidebar */
        width: 220px;  /* Reduced size */
    }

    /* Sidebar background color */
    .css-1lcb1r7 {
        background-color: #2c3e50; /* Darker background color */
    }

    /* Input elements in sidebar */
    .sidebar select, .sidebar input {
        background-color: #2C2C2C;
        border: 1px solid #444;
        color: #EAEAEA;
        padding: 12px;
        font-size: 16px;
        border-radius: 6px;
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }

    .sidebar select:focus, .sidebar input:focus {
        border-color: #00BFFF;
        outline: none;
        box-shadow: 0 0 5px #00BFFF;
    }

    /* Button styling */
    .stButton button {
        background-color: #FF7A00;
        color: white;
        font-size: 20px;
        font-weight: bold;
        padding: 16px 32px;
        border-radius: 12px;
        border: none;
        box-shadow: 0px 5px 20px rgba(255, 122, 0, 0.4);
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .stButton button:hover {
        background-color: #E87C00;
        box-shadow: 0px 8px 30px rgba(255, 122, 0, 0.6);
    }

    .stButton button:active {
        transform: translateY(2px);
    }

    /* Card-like input layout */
    .card {
        padding: 20px;
        background-color: #333;
        border-radius: 10px;
        margin: 20px 0;
        box-shadow: 0px 8px 30px rgba(0, 0, 0, 0.3);
    }

    .card input, .card select {
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# App title and description
st.markdown('<div class="hero"><h1>✨ Car Dheko - Used Car Price Prediction</h1><p>Predict the price of your car based on its specifications and history. 🚗</p></div>', unsafe_allow_html=True)

# Load data and model functions
def load_data():
    if os.path.exists(dataset_path):
        return pd.read_csv(dataset_path)
    else:
        st.error("Dataset not found.")
        return None

def load_model():
    if os.path.exists(model_path):
        return joblib.load(model_path)
    else:
        st.error("Model not found.")
        return None

# Initialize data and model
df = load_data()
pipeline_model = load_model()

if df is not None and pipeline_model is not None:
    st.sidebar.markdown("<p class='sidebar-content'>**Enter Car Specifications**</p>", unsafe_allow_html=True)

    # Sidebar inputs for user specifications in a card-style layout
    with st.sidebar:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        brand = st.selectbox("Car Brand", options=df['Brand'].unique())
        fuel_type = st.selectbox("Fuel Type", ['Petrol', 'Diesel', 'Lpg', 'Cng', 'Electric'])
        body_type = st.selectbox("Body Type", ['Hatchback', 'SUV', 'Sedan', 'MUV', 'Coupe', 'Minivans', 'Convertibles', 'Hybrids', 'Wagon', 'Pickup Trucks'])

        # Model dropdown based on filters
        filtered_models = df[(df['Brand'] == brand) & (df['body type'] == body_type) & (df['Fuel type'] == fuel_type)]['model'].unique()
        if filtered_models.size > 0:
            car_model = st.selectbox("Car Model", options=filtered_models)
        else:
            car_model = st.selectbox("Car Model", options=["No models available"])

        transmission = st.selectbox("Transmission", ['Manual', 'Automatic'])
        seats = st.selectbox("Seats", sorted(df['Seats'].unique()))
        insurance_type = st.selectbox("Insurance Type", ['Third Party insurance', 'Comprehensive', 'Third Party', 'Zero Dep', '2', '1', 'Not Available'])
        color = st.selectbox("Color", df['Color'].unique())
        city = st.selectbox("City", options=df['City'].unique())

        # Numeric inputs
        model_year = st.number_input("Manufacturing Year", min_value=1980, max_value=2025, step=1)
        mileage = st.number_input("Mileage (in km/l)", min_value=1.0, max_value=50.0, step=0.1)
        owner_no = st.number_input("Owner Number", min_value=1, max_value=5, step=1)
        kms_driven = st.number_input("Kilometers Driven", min_value=100, max_value=1000000, step=1000)

        st.markdown('</div>', unsafe_allow_html=True)  # Close card layout

    # Main area predict button
    st.markdown("<br>", unsafe_allow_html=True)
    predict_button = st.button("🚗 Predict Price")

    # Predict
    if predict_button:
        if car_model != "No models available":
            input_data = pd.DataFrame({
                'Fuel type': [fuel_type],
                'body type': [body_type],
                'transmission': [transmission],
                'ownerNo': [owner_no],
                'Brand': [brand],
                "model": [car_model],
                'modelYear': [model_year],
                'Insurance Type': [insurance_type],
                'Kms Driven': [kms_driven],
                'Mileage': [mileage],
                'Seats': [seats],
                'Color': [color],
                'City': [city]
            })

            try:
                prediction = pipeline_model.predict(input_data)
                st.success(f"Estimated Price: ₹ {prediction[0]:,.2f}")
            except Exception as e:
                st.error("Error making prediction.")
        else:
            st.warning("Please select valid options for all fields.")
else:
    st.error("Unable to load data or model.")
