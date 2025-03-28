from flask import Blueprint, render_template, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import os
import gdown


# Google Drive model file ID (Replace this with your actual file ID)
GDRIVE_FILE_ID = "1glxngddSTcXltV5fntyekfRZ1_TZQFP1"

# Model path
MODEL_PATH = "./models/crop_disease_model.h5"

# Ensure the models directory exists
os.makedirs("models", exist_ok=True)

# Function to download the model if it doesn’t exist
def download_model():
    if not os.path.exists(MODEL_PATH):
        print("Downloading crop disease model from Google Drive...")
        url = f"https://drive.google.com/uc?id={GDRIVE_FILE_ID}"
        gdown.download(url, MODEL_PATH, quiet=False)
        print("Download complete.")

# Download model before loading
download_model()

# Load the trained deep learning model
disease_model = tf.keras.models.load_model(MODEL_PATH)

# Define Blueprint correctly
crop_disease_bp = Blueprint("crop_disease", __name__, template_folder='templates')

# disease_model = tf.keras.models.load_model("./models/crop_disease_model.h5")

crop_class = {
    0: 'Apple___Apple_scab', 1: 'Apple___Black_rot', 2: 'Apple___Cedar_apple_rust', 3: 'Apple___healthy',
    4: 'Blueberry___healthy', 5: 'Cherry_(including_sour)___Powdery_mildew', 6: 'Cherry_(including_sour)___healthy',
    7: 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 8: 'Corn_(maize)___Common_rust_', 
    9: 'Corn_(maize)___Northern_Leaf_Blight', 10: 'Corn_(maize)___healthy', 11: 'Grape___Black_rot',
    12: 'Grape___Esca_(Black_Measles)', 13: 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 14: 'Grape___healthy',
    15: 'Orange___Haunglongbing_(Citrus_greening)', 16: 'Peach___Bacterial_spot', 17: 'Peach___healthy',
    18: 'Pepper,_bell___Bacterial_spot', 19: 'Pepper,_bell___healthy', 20: 'Potato___Early_blight',
    21: 'Potato___Late_blight', 22: 'Potato___healthy', 23: 'Raspberry___healthy', 24: 'Soybean___healthy',
    25: 'Squash___Powdery_mildew', 26: 'Strawberry___Leaf_scorch', 27: 'Strawberry___healthy',
    28: 'Tomato___Bacterial_spot', 29: 'Tomato___Early_blight', 30: 'Tomato___Late_blight',
    31: 'Tomato___Leaf_Mold', 32: 'Tomato___Septoria_leaf_spot', 
    33: 'Tomato___Spider_mites Two-spotted_spider_mite', 34: 'Tomato___Target_Spot',
    35: 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 36: 'Tomato___Tomato_mosaic_virus', 37: 'Tomato___healthy'
}

@crop_disease_bp.route("/predict_disease", methods=["GET", "POST"])
def predict_disease():
    result = None  # Ensure result is defined
    confidence = None

    if request.method == "POST":
        file = request.files.get("file")  # Use .get() to avoid KeyError
        if file:
            image = Image.open(io.BytesIO(file.read()))
            image = image.convert("RGB")
            image = image.resize((224, 224))
            image = np.array(image) / 255.0
            image = np.expand_dims(image, axis=0)

            # Make prediction
            prediction = disease_model.predict(image)
            predicted_index = np.argmax(prediction)
            predicted_class = crop_class[predicted_index]
            confidence = round(100 * np.max(prediction), 2)

            # Only show results if confidence is high
            if confidence >= 80:
                result = predicted_class
            else:
                result = "NOT FOUND"

    return render_template("disease-detect.html", result=result, confidence=confidence)
