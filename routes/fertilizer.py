from flask import Blueprint, render_template, request
import pickle
import numpy as np

fertilizer_bp = Blueprint("fertilizer", __name__, template_folder="templates")

# Load the trained ML model
model = pickle.load(open("./models/classifier.pkl", "rb"))
fertilizer = pickle.load(open("./models/fertilizer.pkl", "rb"))



@fertilizer_bp.route('/predict_fertilizer', methods=['GET', 'POST'])
def predict_fertilizer():
    temp = request.form.get('temperature')
    humi = request.form.get('humidity')
    mois = request.form.get('moisture')
    soil = request.form.get('soilType')
    crop = request.form.get('cropType')
    nitro = request.form.get('nitrogen')
    pota = request.form.get('potassium')
    phosp = request.form.get('phosphorous')

    # Check if any value is None or empty
    if None in (temp, humi, mois, soil, crop, nitro, pota, phosp) or any(val.strip() == "" for val in (temp, humi, mois, soil, crop, nitro, pota, phosp)):
        return render_template('fertilizer-recommendation.html', x='Invalid input. Please provide numeric values for all fields.')

    # Convert values to integers safely
    try:
        input_values = [int(temp), int(humi), int(mois), int(soil), int(crop), int(nitro), int(pota), int(phosp)]
    except ValueError:
        return render_template('fertilizer-recommendation.html', x='Invalid input. Please enter valid numeric values.')

    # Make predictions
    res = fertilizer.classes_[model.predict([input_values])]
    return render_template('fertilizer-recommendation.html', x=res[0])

