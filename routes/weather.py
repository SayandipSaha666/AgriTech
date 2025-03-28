from flask import Blueprint, render_template, request, jsonify
import requests

weather_bp = Blueprint('weather', __name__)

@weather_bp.route('/weather', methods=['GET', 'POST'])
def weather():
    if request.method == 'POST':
        location = request.form.get('location')


        if not location:
            return jsonify({"error": "Location required"}), 400

        API_KEY = "0ac0d7809f87912b8c04c42cf3137c3c"  # Replace with your OpenWeatherMap API key
        response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}")

        return jsonify(response.json())

    return render_template("weather.html")
