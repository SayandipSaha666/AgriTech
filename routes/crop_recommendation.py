from flask import Blueprint, render_template, request
import pickle
import numpy as np

crop_recommendation_bp = Blueprint("crop_recommendation", __name__, template_folder="templates")

# Load the trained ML model
model = pickle.load(open("./models/model1.pkl", "rb"))
sc = pickle.load(open("./models/StandardScaler.pkl", "rb"))
mx = pickle.load(open("./models/MinMaxScaler.pkl", "rb"))

@crop_recommendation_bp.route("/recommend_crop", methods=["GET", "POST"])
def recommend_crop():
    if request.method == "GET":
        return render_template("crop-preferences.html", result=None)
    elif request.method == "POST":
        temp = request.form.get("temp")
        humidity = request.form.get("humidity")
        rainfall = request.form.get("rainfall")
        nitro = request.form.get("N")
        phos = request.form.get("P")
        pota = request.form.get("K")
        pH = request.form.get("pH")

        feature_list = [nitro, phos, pota, temp, humidity, pH, rainfall]
        single_pred = np.array(feature_list).reshape(1, -1)

        mx_features = mx.transform(single_pred)
        sc_mx_features = sc.transform(mx_features)
        prediction = model.predict(sc_mx_features)

        crop_dict = {
            1: "Rice", 2: "Maize", 3: "Jute", 4: "Cotton", 5: "Coconut", 6: "Papaya", 7: "Orange",
            8: "Apple", 9: "Muskmelon", 10: "Watermelon", 11: "Grapes", 12: "Mango", 13: "Banana",
            14: "Pomegranate", 15: "Lentil", 16: "Blackgram", 17: "Mungbean", 18: "Mothbeans",
            19: "Pigeonpeas", 20: "Kidneybeans", 21: "Chickpea", 22: "Coffee"
        }

        if prediction[0] in crop_dict:
            crop = crop_dict[prediction[0]]
            result = f"{crop} is the best crop to be cultivated right there."
        else:
            result = "Sorry, we could not determine the best crop to be cultivated with the provided data."

        return render_template("crop-preferences.html", result=result)

