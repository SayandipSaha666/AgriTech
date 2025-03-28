from flask import Flask, render_template, request, redirect, url_for
import os
import gdown

from routes.crop_recommendation import crop_recommendation_bp
from routes.crop_disease import crop_disease_bp
from routes.fertilizer import fertilizer_bp
from routes.weather import weather_bp

app = Flask(__name__, template_folder='templates')

# Registering Blueprints (Modularized Routes)
app.register_blueprint(crop_recommendation_bp)
app.register_blueprint(crop_disease_bp)
app.register_blueprint(fertilizer_bp)
app.register_blueprint(weather_bp)


# Google Drive model file ID
GDRIVE_FILE_ID = "1glxngddSTcXltV5fntyekfRZ1_TZQFP1"  # Change this to your actual file ID
MODEL_PATH = "./models/crop_disease_model.h5"

# Ensure models directory exists
os.makedirs("models", exist_ok=True)

# Function to download the model from Google Drive if not present
def download_model():
    if not os.path.exists(MODEL_PATH):  # Check if model already exists
        print("Downloading model from Google Drive...")
        url = f"https://drive.google.com/uc?id={GDRIVE_FILE_ID}"
        gdown.download(url, MODEL_PATH, quiet=False)
        print("Download complete.")

# Call download function on startup
download_model()

# Home Page Route
@app.route("/")
def home():
    return render_template("index.html")

@app.route('/index.html')
def index_page():
    return redirect(url_for('home'))

@app.route('/recommend_crop', methods=['GET', 'POST'])
def crop_recommend():
    return render_template('crop-preferences.html')

@app.route('/crop-preferences.html')
def feature1():
    return redirect(url_for('crop_recommendation.recommend_crop'))

@app.route('/disease_detect', methods=['GET', 'POST'])
def disease_detect():
    return render_template('disease-detect.html')

@app.route('/disease-detect.html')
def feature2():
    return redirect(url_for('crop_disease.predict_disease'))

@app.route('/fertilizer_recommend', methods=['GET', 'POST'])
def fertilizer():
    return render_template('fertilizer-recommendation.html')

@app.route('/fertilizer-recommendation.html')
def feature3():
    return redirect(url_for('fertilizer.predict_fertilizer'))

@app.route('/weather', methods=['GET', 'POST'])
def weather_page():
    return render_template('weather.html')

@app.route('/weather.html')
def feature4():
    return redirect(url_for('weather.weather'))

if __name__ == "__main__":
    app.run(debug=True)


