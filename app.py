from flask import Flask, render_template, request
import pandas as pd
import joblib
import os
print("current Working Directory:",os.getcwd())
print('Files:',os.listdir())

app = Flask(__name__)

# ===========================
# Load Model and Scaler
# ===========================

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(BASE_DIR, "catboost_model.pkl")
scaler_path = os.path.join(BASE_DIR, "robust_scaler.pkl")

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)
# ===========================
# Label Encoder Mappings
# ===========================

location_map = {
    "Delhi": 0,
    "Gurugram": 1,
    "Indore": 2,
    "Jaipur": 3,
    "Kanpur": 4,
    "Lucknow": 5,
    "Noida": 6,
    "Prayagraj": 7
}

street_map = {
    "Corner Plot": 0,
    "Gated Society": 1,
    "Highway Facing": 2,
    "Main Road": 3,
    "Residential Lane": 4
}

furnishing_map = {
    "Furnished": 0,
    "Not Furnished": 1,
    "Semi Furnished": 2
}

property_map = {
    "Apartment": 0,
    "Duplex": 1,
    "Independent House": 2,
    "Villa": 3
}

pool_map = {
    "No": 0,
    "Yes": 1
}

# ===========================
# Home Page
# ===========================

@app.route("/")
def home():
    return render_template("index.html")

# ===========================
# Prediction
# ===========================

@app.route("/predict", methods=["POST"])
def predict():

    area = float(request.form["Area_SqFt"])
    rooms = int(request.form["Rooms"])
    build_year = int(request.form["Build_Year"])

    location = location_map[request.form["Location"]]
    street = street_map[request.form["Street_Type"]]
    furnishing = furnishing_map[request.form["Furnishing"]]
    property = property_map[request.form["Property_Type"]]
    pool = pool_map[request.form["Has_Pool"]]

    input_data = pd.DataFrame({

        "Area_SqFt": [area],
        "Rooms": [rooms],
        "Build_Year": [build_year],
        "Location": [location],
        "Street_Type": [street],
        "Furnishing": [furnishing],
        "Property_Type": [property],
        "Has_Pool": [pool]

    })

    input_scaled = scaler.transform(input_data)

    prediction = model.predict(input_scaled)[0]

    prediction = "$ {:,.2f}".format(prediction)

    return render_template(
        "index.html",
        prediction_text=prediction
    )

# ===========================
# Run Flask
# ===========================

if __name__ == "__main__":
    app.run(debug=True)